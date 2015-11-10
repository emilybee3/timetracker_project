# this page has Flask routes
"""Time Tracker."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify

from model import connect_to_db, db, User, Response

from datetime import datetime, date

import json

from isoweek import Week


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

#################################################################################
##################################LOGIN############################################


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
        return redirect("/login")

    #check for correct password
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    #add logged in user to session
    session["user_id"] = user.user_id

    #give user feedback
    flash("Logged in")
    return redirect("/chart")

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
    print email
    password = request.form["password"]
    print password
    phone = request.form["phone"]
    print phone
    name = request.form["name"]
    print name

    #see if user is already in database
    user = User.query.filter_by(email=email).first()

    if user:
        flash("You already have an account")
        return redirect("/login")

    #create a new user from form info
    new_user = User(email=email, password=password, name=name, phone=phone)

    #add user to db
    db.session.add(new_user)
    print "I've added your user!"

    #commit new user to db
    db.session.commit()
    print "I've commited your user!"

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

    #convert date into isocalendar to pull out date of Monday and Sunday
    iso_date = datetime.isocalendar(date)
    year = iso_date[0]
    week = iso_date[1]
    monday = Week(year, week).monday()
    sunday = Week(year, week).sunday()

    #query database for data from current week and signed in user
    query = (db.session.query(Response.response_id,
                              Response.day,
                              Response.text,
                              Response.time_interval,
                              Response.color)
             .filter(Response.user_id == session["user_id"], Response.date >= monday,
                     Response.date <= sunday)
             .all())

    #create json dictionary from query responses, append to list
    to_json = []

    for item in query:
        response_dict = {"response_id": item[0],
                         "day": item[1],
                         "words": item[2],
                         "hour": item[3],
                         "value": item[4]}

        to_json.append(response_dict)

    #return json data object of list containing json dictionary
    return jsonify(data=to_json)


@app.route("/pickweek", methods=['POST'])
def pickweek():
    """Process chosen date inputted from user and returns data for that week to chart"""

    #get date from form on mainpage
    formdate = request.form.get("date")
    #turn date from mainpage into a datetime object
    date = datetime.strptime(formdate, "%Y-%m-%d")

    #convert date into isocalendar to pull out date of Monday and Sunday
    iso_date = datetime.isocalendar(date)
    year = iso_date[0]
    week = iso_date[1]
    monday = Week(year, week).monday()
    sunday = Week(year, week).sunday()

    #query database for data from chosen week and signed in user
    query = (db.session.query(Response.response_id,
                              Response.day,
                              Response.text,
                              Response.time_interval,
                              Response.color)
             .filter(Response.user_id == session["user_id"], Response.date >= monday,
                     Response.date <= sunday)
             .all())

    #create json dictionary from query responses
    to_json = []

    for item in query:
        response_dict = {"response_id": item[0],
                         "day": item[1],
                         "words": item[2],
                         "hour": item[3],
                         "value": item[4]}

        to_json.append(response_dict)

    #return json data object of list containing json dictionary
    return jsonify(data=to_json)



################################################################################
#############################RESPONSE FORM######################################


@app.route('/response', methods=['GET'])
def show_form():
    """Show timetracker form"""
    return render_template("form.html")


@app.route('/response', methods=['POST'])
def submit_form():
    """Process timetracker form"""

    # get form variables
    hourint = request.form["hourint"]
    text = request.form["text"]
    color = request.form["color"]

    #set date to now
    date = datetime.now()

    #extract day from datetime stamp
    iso_week = datetime.isocalendar(date)
    day = iso_week[2]

    #set user_id to logged in user
    user_id = session["user_id"]

    #create a new response
    new_response = Response(user_id=user_id, color=color, date=date, day=day, time_interval=hourint, text=text)

    #add new response to database
    db.session.add(new_response)
    db.session.commit()
    print "I've commited your response!"

    return redirect("/chart")

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
