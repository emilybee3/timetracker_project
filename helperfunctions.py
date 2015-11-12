from model import connect_to_db, db, User, Response
from datetime import datetime, date, time
from isoweek import Week
from flask import session, jsonify
import unittest

def get_monday_sunday(date):
    """convert date into isocalendar to pull out date of Monday and Sunday"""
    iso_date = datetime.isocalendar(date)
    year = iso_date[0]
    week = iso_date[1]
    monday_no_time = Week(year, week).monday()
    monday = datetime.combine(monday_no_time, datetime.min.time())
    sunday_no_time = Week(year, week).sunday()
    sunday = datetime.combine(sunday_no_time, datetime.min.time())


    return monday, sunday
