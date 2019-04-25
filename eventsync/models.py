"""
Database Models go here
"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    username = db.Column(db.String(30), nullable=False, primary_key=True)
    pw_hash = db.Column(db.LargeBinary(60), nullable=False)

    events = db.relationship("Event", backref="Creator", cascade="all")
    items = db.relationship("Item", backref="Claimer")

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

    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def get_all_but_user(username):
        return User.query.filter(User.username != username).all()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    creator = db.Column(db.String(30), db.ForeignKey("user.username"), nullable=False)
    description = db.Column(db.String(150), default="", nullable=False)
    date_time = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    items = db.relationship("Item", backref="Event", cascade="all")

    @staticmethod
    def get_all():
        return Event.query.all()

    @staticmethod
    def get_event(event_id):
        """Returns a Event Object for a specific event, if it exists.

        Args:
            event_id: event_id to search for
        """
        return Event.query.filter_by(id=event_id).first()

    def save(self):
        """Addes the non-existing event to the DB."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the event from the DB."""
        db.session.delete(self)
        db.session.commit()


"""
    Needed Tables:

        items: Items that belong to a specific event
        belongs_to: user ids of users belonging to an event id
        tags: string tags of items "Dessert" or "Drink"
        invites: pending invites
"""


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    claimedBy = db.Column(db.String(30), db.ForeignKey("user.username"), nullable=False)
    claimed = db.Column(db.Boolean, default=False, nullable=False)
    eventID = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    # tags = db.relationship("tags", backref="Item", cascade="all")


class BelongTo(db.Model):
    username = db.Column(
        db.String(30), db.ForeignKey("user.username"), primary_key=True, nullable=False
    )
    eventID = db.Column(
        db.Integer, db.ForeignKey("event.id"), primary_key=True, nullable=False
    )
    accepted = db.Column(db.Boolean, default=False, nullable=False)

    @staticmethod
    def get_all():
        return BelongTo.query.all()

    @staticmethod
    def get_accepted():
        accepted = BelongTo.query.filter_by(accepted=True).all()
        if len(accepted) == 0:
            return None
        return accepted

    @staticmethod
    def get_pending():
        pending = BelongTo.query.filter_by(accepted=False).all()
        if len(pending) == 0:
            return None
        return pending

# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), default="", nullable=False)


# tags = db.Table(
#     "tags",
#     db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
#     db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
# )

