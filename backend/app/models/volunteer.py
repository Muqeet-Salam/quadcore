from app import db
from .User import User
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy import func

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
    rating = db.Column(db.Float)

    # Add this relationship
    ratings_received = relationship("VolunteerMatch", back_populates="volunteer")

    __mapper_args__ = {
        'polymorphic_identity': 'volunteer',
    }

    def __repr__(self):
        return f'<Volunteer {self.email}>'

    def update_average_rating(self):
        avg_rating = db.session.query(func.avg(VolunteerMatch.volunteer_rating)).filter(VolunteerMatch.volunteer_id == self.id).scalar()
        self.rating = avg_rating
        db.session.commit()

    @classmethod
    def get_volunteers_with_ratings(cls):
        return cls.query.filter(cls.rating.isnot(None)).all()
