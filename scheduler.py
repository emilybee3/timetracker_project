from model import connect_to_db, db, User, Response
from flask import Flask
from flask import render_template, session
from server import app
from apscheduler.schedulers.blocking import BlockingScheduler
import time
from flask_mail import Mail
from flask.ext.mail import Message
import config
import logging
logging.basicConfig()
from server import get_signedin_email
from flask.ext.sqlalchemy import SQLAlchemy

def get_emails():
    emails = db.session.query(User.email).all()
    for email in emails:
        print email[0]

def sendemail():
    """sends emails and handles scheduling"""

    msg = Message('Your reminder!', sender=config.ADMINS[0], recipients=config.ADMINS)
    msg.body = 'text body'
    msg.html = '''<p> Its time to track your time! Please visit http://localhost:5000/response
        to fill out your activity tracker form :D
    </p>

    <p>To unsubscribe from these emails, please visit http://localhost:5000/response
        and deselect the "Get Reminder Emails" checkbox </p>'''

    with app.app_context():
        mail.send(msg)

    # return render_template("instructions.html")

def send_emails():

    localtime = time.localtime()
    current_hour = localtime.tm_hour

    if (current_hour > 8 and current_hour < 21):
        sendemail()
        print "I've sent an email!"


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    get_signedin_email()
    scheduler = BlockingScheduler()
    scheduler.add_job(send_emails, 'interval', seconds=20)
    scheduler.start()
    mail = Mail(app)
