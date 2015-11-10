# this page has Flask routes
"""Time Tracker."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

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


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("mainlogin.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    print email
    password = request.form["password"]
    print password

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No users match this email address")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/response")

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

    user = User.query.filter_by(email=email).first()

    if user:
        flash("You already have an account")
        return redirect("/login")

    new_user = User(email=email, password=password, name=name, phone=phone)
    print new_user

    db.session.add(new_user)
    print "I've added your user!"
    db.session.commit()
    print "I've commited your user!"

    session["user_id"] = user.user_id

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

@app.route("/")
def mainpage():
    """Main page"""
    return render_template("mainpage.html")


@app.route("/pickweek", methods=['POST'])
def pickweek():

    formdate = request.form.get("date")
    date = datetime.strptime(formdate, "%Y-%m-%d")
    iso_date = datetime.isocalendar(date)
    year = iso_date[0]
    week = iso_date[1]

    monday = Week(year, week).monday()
    sunday = Week(year, week).sunday()
    # Query db to get > day 1 < day 7 (check oratings)

    query = (db.session.query(Response.response_id,
                              Response.day,
                              Response.text,
                              Response.time_interval,
                              Response.color)
             .filter(Response.user_id == session["user_id"], Response.date >= monday,
                     Response.date <= sunday)
             .all())
    to_json = []

    for item in query:
        response_dict = {"response_id": item[0],
                         "day": item[1],
                         "words": item[2],
                         "hour": item[3],
                         "value": item[4]}

        to_json.append(response_dict)

    print to_json
    return jsonify(data=to_json)


@app.route("/sendjson")
def send_json():

    date = datetime.now()
    iso_date = datetime.isocalendar(date)
    year = iso_date[0]
    week = iso_date[1]

    monday = Week(year, week).monday()
    sunday = Week(year, week).sunday()

    query = (db.session.query(Response.response_id,
                              Response.day,
                              Response.text,
                              Response.time_interval,
                              Response.color)
             .filter(Response.user_id == session["user_id"], Response.date >= monday,
                     Response.date <= sunday)
             .all())
    to_json = []

    for item in query:
        response_dict = {"response_id": item[0],
                         "day": item[1],
                         "words": item[2],
                         "hour": item[3],
                         "value": item[4]}

        to_json.append(response_dict)

    print to_json
    return jsonify(data=to_json)


################################################################################
#############################RESPONSE FORM######################################

@app.route('/response', methods=['GET'])
def show_form():
    return render_template("form.html")


@app.route('/response', methods=['POST'])
def submit_form():
    """Process form"""
    # this will change to store datetimes instead of isotime --cmd

    print "route reached"
    # Get form variables
    hourint = request.form["hourint"]
    print "hourint: ", hourint
    text = request.form["text"]
    print "text: ", text
    color = request.form["color"]
    print "color: ", color
    #deal with date
    date = datetime.now()
    iso_week = datetime.isocalendar(date)
    day = iso_week[2]

    # date_str = date_now.strftime("%A, %B %d, %Y")
    # date = datetime.strptime(date_str, "%A, %B %d, %Y")
    print date

    user_id = session["user_id"]

    print "I should have printed all the things"

    new_response = Response(user_id=user_id, color=color, date=date, day=day, time_interval=hourint, text=text)
    print new_response

    db.session.add(new_response)
    print "I've added your response!"
    db.session.commit()
    print "I've commited your response!"

    # flash("Response- %s added." % text)

    return redirect("/")

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
