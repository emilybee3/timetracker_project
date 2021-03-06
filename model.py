# this page has my data model

from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

db = SQLAlchemy()


##############################################################################
# Model definitions


class User(db.Model):
    """User of time tracking website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Response(db.Model):
    """Responses from time tracker website's main tracking form."""

    __tablename__ = "responses"

    response_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    time_interval = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    day = db.Column(db.Integer)
    text = db.Column(db.String(400))
    color = db.Column(db.String(10), nullable=False)

# Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("responses", order_by=response_id))

    def to_d3_dict(self):
        return {"response_id": self.response_id,
                "day": self.day,
                "words": self.text,
                "hour": self.time_interval,
                "value": self.color}

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Time Interval=%s Day=%s DATE=%s text=%s color=%s>" % (self.time_interval, self.day, self.date, self.text, self.color)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetracker.db'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
