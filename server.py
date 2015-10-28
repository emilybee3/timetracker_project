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


@app.route('/')
def show_form():
    """Form"""
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

    print "I should have printed all the things"

    new_response = Response(color=color, date=date, time_interval=hourint, text=text)
    print new_response

    db.session.add(new_response)
    print "I've added your response!"
    db.session.commit()
    print "I've commited your response!"

    # flash("Response- %s added." % text)

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
