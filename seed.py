"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import datetime

from model import User, Response, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        user_id, name, email, password, phone = row.split("|")

        user = User(user_id=user_id,
                    name=name,
                    email=email,
                    password=password,
                    phone=phone)

        # add to the session
        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_responses():
    """Load responses from u.responses into database."""

    print "Responses"

    for i, row in enumerate(open("seed_data/u.responses")):
        row = row.rstrip()
        # print row

        # clever -- we can unpack part of the row!
        response_id, user_id, time_interval, date, text, color = row.split("|")
        print row.split("|")

        # The date is in the file as daynum-month_abbreviation-year;
        # we need to convert it to an actual datetime object.

        # date_obj = datetime.datetime.strptime(date, "%Y-%W-%u")


        response = Response(response_id=response_id,
                      user_id=user_id,
                      time_interval=time_interval,
                      date=date,
                      text=text,
                      color=color)

        # We need to add to the session or it won't ever be stored
        db.session.add(response)

        # provide some sense of progress
        # if i % 100 == 0:
            # print i

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_responses()
