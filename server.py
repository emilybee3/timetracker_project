# this page has Flask routes
"""Time Tracker"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify

from model import connect_to_db, db, User, Response

from datetime import datetime, date, time

import json

from isoweek import Week

from helperfunctions import get_monday_sunday

from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

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


@app.route("/search", methods=['POST'])
def search():
    """handles search function"""
    # print "HELLO WE PINGED HERE"
    keyword = request.form.get("keyword")
    print keyword
    # return "this is a string"

    date = datetime.now()
    monday, sunday = get_monday_sunday(date)#call helper function that converts dates
    print monday, sunday

    week_data_query = (db.session.query(Response)
                       .filter(Response.user_id == session["user_id"],
                               Response.date >= monday,
                               Response.date <= sunday).all())
    # print week_data_query
    #create json dictionary from query responses, append to list
    to_json = []


    for response in week_data_query:
        # print response
        if keyword in response.text:
            # new_response = response
            # print new_response.color
            response_dict = response.to_d3_dict()
            # print response_dict
            response_dict["color"] = "#0066ff"
            # print response_dict

            to_json.append(response_dict)
            # print to_json


    #return json data object of list containing json dictionary
    return jsonify(data=to_json)



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
                       .filter(Response.user_id == session["user_id"], Response.date >= monday,
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
    old_date = datetime.now()
    stripped_date = datetime.date(old_date)
    date = datetime.combine(stripped_date, datetime.min.time())
    print date

    #extract day from datetime stamp
    iso_week = datetime.isocalendar(date)
    day = iso_week[2]

    #set user_id to logged in user
    user_id = session["user_id"]

    #see if there is already a response with the same day and time id in db
    test_response = Response.query.filter(Response.date == date, Response.time_interval == hourint).all()

    if test_response:
        flash("You already submitted a response for that time period")
        return redirect("/response")

    # create a new response
    new_response = Response(user_id=user_id, color=color, date=date, day=day, time_interval=hourint, text=text)

    # add new response to database
    db.session.add(new_response)
    db.session.commit()
    # print "I've commited your response!"

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
