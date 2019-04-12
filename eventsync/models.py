"""
Database Models go here
"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(30), nullable=False, primary_key=True)
    pw_hash = db.Column(db.Binary(60), nullable=False)

    events = db.relationship("Event", backref="Creator", cascade="all")

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_authenticated(self):
        """Anytime this User class is instantiated,
        the user is authenticated...
        """
        return True

    def get_id(self):
        return str(self.username)

    def save(self):
        """Addes the non-existing user to the DB."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the user from the DB."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_user(username):
        """Returns a user Object for a specific user, if it exists.

        Args:
            username: username to search for
        """
        return User.query.filter_by(username=username).first()


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    creator = db.Column(db.String(30), db.ForeignKey("users.username"), nullable=False)
    date_time = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    def save(self):
        """Addes the non-existing event to the DB."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the event from the DB."""
        db.session.delete(self)
        db.session.commit()


# class Friend(db.Model):
#     __tablename__ = "friends"
