import unittest
from helperfunctions import get_monday_sunday
from model import Response, connect_to_db, db, User
from datetime import datetime, date
from server import app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask



class WeekDataTest(unittest.TestCase):

    def test_week_data(self):
        """does this successfully pull the start and end dates of a given week?"""
        input_date = "2015-02-04"
        input_date_obj = datetime.strptime(input_date, "%Y-%m-%d")

        monday = datetime.strptime("2015, 2, 2", "%Y, %m, %d")
        # monday_obj = datetime.date(monday)
        sunday = datetime.strptime("2015, 2, 8", "%Y, %m, %d")
        # sunday_obj = datetime.date(sunday)

        self.assertEqual(get_monday_sunday(input_date_obj), (monday, sunday))

    def test_week_data_given_a_monday(self):
        """does this successfully pull the start and end dates of a
           given week given a monday?"""

        input_date = "2015-02-16"
        input_date_obj = datetime.strptime(input_date, "%Y-%m-%d")
        monday = datetime.strptime("2015, 2, 16", "%Y, %m, %d")
        # monday_obj = datetime.date(monday)
        sunday = datetime.strptime("2015, 2, 22", "%Y, %m, %d")
        # sunday_obj = datetime.date(sunday)

        self.assertEqual(get_monday_sunday(input_date_obj), (monday, sunday))


    def test_week_data_given_a_sunday(self):
            """does this successfully pull the start and end dates of a
               given week given a sunday?"""

            input_date = "2015-02-22"
            input_date_obj = datetime.strptime(input_date, "%Y-%m-%d")
            monday = datetime.strptime("2015, 2, 16", "%Y, %m, %d")
            # monday_obj = datetime.date(monday)
            sunday = datetime.strptime("2015, 2, 22", "%Y, %m, %d")
            # sunday_obj = datetime.date(sunday)

            self.assertEqual(get_monday_sunday(input_date_obj), (monday, sunday))

class ResponseMethodTests(unittest.TestCase):

    def test_dictionary_creation(self):
        """given query response, is a json dictionary created?"""

        #create fake response
        hourint = 1
        text = "This is some text"
        color = "green"
        date_obj = datetime.strptime("2015, 2, 16", "%Y, %m, %d")
        date= datetime.date(date_obj)
        iso_week = datetime.isocalendar(date)
        day = iso_week[2]
        user_id = 5000

        new_response = Response(user_id=user_id, color=color, date=date, day=day, time_interval=hourint, text=text)

        #add and commit it to my database
        db.session.add(new_response)
        db.session.commit()

        #query for that data
        query = db.session.query(Response).filter_by(user_id = 5000).first()
        print query
        #write out what that query jsonified would look like

        json_dict = {
            "response_id": 1,
            "day": 2,
            "words": "This is some text",
            "hour": 1,
            "value": "green"
        }

        #pass that query data to to_d3_dict for comparison
        self.assertEqual(query.to_d3_dict()["words"], json_dict["words"])
        #rollback database to get rid of new fake response (db.session.rollback())
        db.session.rollback()






#test login
#create a fake user
#commit fake user to database 
#write out what that should look like if querying the database
#compare giving that information to login function with what i wrote out


# class WeekDataTest(unittest.TestCase):

#     def setUp(self):
#         self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
#         flaskr.app.config['TESTING'] = True
#         self.app = flaskr.app.test_client()
#         flaskr.init_db()

#     def tearDown(self):
#         os.close(self.db_fd)
#         os.unlink(flaskr.app.config['DATABASE'])
    
#     def login(self, username, password):
#         return self.app.post('/', data=dict(
#             username=username,
#             password=password
#         ), follow_redirects=True)

#     def logout(self):
#         return self.app.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    connect_to_db(app)
    unittest.main()
