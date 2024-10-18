from . import db
from .ser import User
from sqlalchemy.dialects.postgresql import ARRAY

class Volunteer(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    occupation = db.Column(db.String(100))
    interests = db.Column(ARRAY(db.String(50)))  # Array of interests
    availability = db.Column(db.JSON)  # JSON object for flexible availability storage
    skills = db.Column(ARRAY(db.String(50)))  # Array of skills
    profile_urls = db.Column(db.JSON)  # JSON object for various profile URLs
    bio = db.Column(db.Text)
    past_experience = db.Column(db.Text)
    preferred_locations = db.Column(ARRAY(db.String(100)))
    languages = db.Column(ARRAY(db.String(50)))
    time_zone = db.Column(db.String(50))
    notification_preferences = db.Column(db.JSON)
    certificates = db.Column(ARRAY(db.String(100)))
    preferences = db.Column(db.JSON)  # For storing user preferences
    emergency_contact = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity': 'volunteer',
    }

    def __repr__(self):
        return f'<Volunteer {self.email}>'
