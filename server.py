# this page has Flask routes
"""Time Tracker"""
import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from model import connect_to_db, db, User, Response
from datetime import datetime, date, time
import json
from isoweek import Week
from helperfunctions import get_monday_sunday
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask.ext.mail import Message
import config
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

app = Flask(__name__)

app.config.update(
    #EMAIL SETTINGS
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD
)
mail = Mail(app)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

TIMES = [{"hour": "6am - 8am", "time_interval": 1}, {"hour": "8 am - 9 am", "time_interval": 2},
         {"hour": "9 am - 10 am", "time_interval": 3}, {"hour": "10 am - 11 am", "time_interval": 4},
         {"hour": "11 am - 12 pm", "time_interval": 5}, {"hour": "12 pm - 1 pm", "time_interval": 6},
         {"hour": "1 pm - 2 pm", "time_interval": 7}, {"hour": "2 pm - 3 pm", "time_interval": 8},
         {"hour": "3 pm - 4 pm", "time_interval": 9}, {"hour": "4 pm - 5 pm", "time_interval": 10},
         {"hour": "5 pm - 6 pm", "time_interval": 11}, {"hour": "6 pm - 7 pm", "time_interval": 12},
         {"hour": "7 pm - 8 pm", "time_interval": 13}, {"hour": "8 pm - 9 pm", "time_interval": 14},
         {"hour": "9 pm - 11 pm", "time_interval": 15}]


#################################################################################
##################################LOGIN/ LOGOUT############################################


@app.route('/', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("mainlogin.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    #see if user is in db
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No users match this email address")
        return redirect("/")

    #check for correct password
    if user.password != password:
        flash("Incorrect password")
        return redirect("/")

    #add logged in user to session
    session["user_id"] = user.user_id

    #give user feedback
    flash("Logged in")
    return redirect("/chart")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

###############################################################################
######################################SIGN UP###################################


@app.route('/signup', methods=['GET'])
def show_signup():
    """Show sign up page"""

    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup_process():
    """Process sign up."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]
    name = request.form["name"]

    #see if user is already in database
    user = User.query.filter_by(email=email).first()

    if user:
        flash("You already have an account")
        return redirect("/")

    #create a new user from form info
    new_user = User(email=email, password=password, name=name, phone=phone)

    #add user to db
    db.session.add(new_user)
    # print "I've added your user!"

    #commit new user to db
    db.session.commit()
    # print "I've commited your user!"

    #add user to session
    session["user_id"] = user.user_id

    #give user feedback
    flash("You've Signed Up!")
    return redirect("/instructions")


################################################################################
####################################INSTRUCTIONS################################

@app.route('/instructions', methods=['GET'])
def show_instructions():
    """Show sign up page"""
    return render_template("instructions.html")

################################################################################
###################################MAIN PAGE####################################


@app.route("/chart")
def mainpage():
    """Main page with chart"""

    return render_template("mainpage.html")


@app.route("/sendjson")
def send_json():
    """Send current week of JSON data for signed in user to chart"""
    #figure out the start and end dates of the week based on the Monday and Sunday of that week
    date = datetime.now()
    monday, sunday = get_monday_sunday(date)#call helper function that converts dates

    week_data_query = (db.session.query(Response)
                       .filter(Response.user_id == session["user_id"],
                               Response.date >= monday,
                               Response.date <= sunday).all())
    # print week_data_query
    #create json dictionary from query responses, append to list
    to_json = []

    for response in week_data_query:
        to_json.append(response.to_d3_dict())


    #return json data object of list containing json dictionary
    return jsonify(data=to_json)



@app.route("/pickweek", methods=['POST'])
def pickweek():
    """Process chosen date inputted from user and returns data for that week to chart"""

    #get date from form on mainpage
    formdate = request.form.get("date")
    #turn date from mainpage into a datetime object
    date = datetime.strptime(formdate, "%Y-%m-%d")

    monday, sunday = get_monday_sunday(date)#call helper function that converts dates
    print monday, sunday

    week_data_query = (db.session.query(Response)
                       .filter(Response.user_id == session["user_id"], 
                               Response.date >= monday,
                               Response.date <= sunday).all())
    # print week_data_query
    #create json dictionary from query responses
    to_json = []


    for response in week_data_query:
        to_json.append(response.to_d3_dict())

    #return json data object of list containing json dictionary
    return jsonify(data=to_json)


################################################################################
#############################RESPONSE FORM######################################


@app.route('/response', methods=['GET', 'POST'])
def submit_form():
    """Show and Process timetracker form"""
########################################Show Proper Form########################################################    
    #set date
    old_date = datetime.now()
    stripped_date = datetime.date(old_date)
    date = datetime.combine(stripped_date, datetime.min.time())

    #extract day from datetime stamp
    iso_week = datetime.isocalendar(date)
    day = iso_week[2]

    #set user_id to logged in user
    user_id = session["user_id"]

    #see if there is already a response with the same day and time id in db
    test_response = (db.session.query(Response.time_interval)
                     .filter(Response.date == date,
                             Response.user_id == session["user_id"]).all())
    #create a list of the time intervals from above query
    used_times = [item[0] for item in test_response]  #list comprehension omg

    #only display times that haven't already been filled out
    if request.method == 'GET':
        return render_template("form.html", times=TIMES, used_times=used_times)

#######################################Process form################################################################################ 
    else:
        # get form variables
        hourint = request.form["hourint"]
        text = request.form["text"]
        color = request.form["color"]

        # create a new response
        new_response = (Response(user_id=user_id, color=color, date=date, day=day,
                                 time_interval=hourint, text=text))

        # add new response to database
        db.session.add(new_response)
        db.session.commit()

        return redirect("/chart?times="+",".join(str(x) for x in TIMES))

################################################################################
#############################Email Notifications######################################
@app.route("/email")
def sendemail():
    """sends emails and handles scheduling"""

    msg = Message('Your reminder!', sender=config.ADMINS[0], recipients=config.ADMINS)
    msg.body = 'text body'
    msg.html = '<b>Its time to track your time! Please visit:"http://localhost:5000/response"</b>'
    with app.app_context():
        mail.send(msg)

def send_emails():
    sendemail()
    print "I've sent an email!"

scheduler.add_job(send_emails, 'interval', seconds=60)
scheduler.start()

################################################################################
################################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
