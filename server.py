# this page has Flask routes
"""Time Tracker."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Response

from datetime import datetime, date



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

@app.route("/mainpage")
def mainpage():
    """Main page"""
    return render_template("mainpage.html")
# 
# @app.route("/mainpage")
# def populate_mainpage():

    # name = User.query.filter_by(user_id=1).first()
    # return render_template("mainpage.html", name=name)

################################################################################
#############################RESPONSE FORM######################################


@app.route('/response', methods=['GET'])
def show_form():
    return render_template("form.html")


@app.route('/response', methods=['POST'])
def submit_form():
    """Process form"""
    print "route reached"
    # Get form variables
    hourint = request.form["hourint"]
    print "hourint: ", hourint
    text = request.form["text"]
    print "text: ", text
    color = request.form["color"]
    print "color: ", color
    #deal with date
    date_now = datetime.now()
    date_str = date_now.strftime("%A, %B %d, %Y")
    date = datetime.strptime(date_str, "%A, %B %d, %Y")
    print date

    user_id = session["user_id"]

    print "I should have printed all the things"

    new_response = Response(user_id=user_id, color=color, date=date, time_interval=hourint, text=text)
    print new_response

    db.session.add(new_response)
    print "I've added your response!"
    db.session.commit()
    print "I've commited your response!"

    # flash("Response- %s added." % text)

    return redirect("/mainpage")

################################################################################
################################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
