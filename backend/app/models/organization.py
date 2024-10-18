from . import db
from .User import User
from sqlalchemy.dialects.postgresql import ARRAY

class Organization(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    org_name = db.Column(db.String(100), nullable=False)
    org_url = db.Column(db.String(200))
    description = db.Column(db.Text)
    profile_urls = db.Column(db.JSON)  # JSON object for various profile URLs
    contact_person = db.Column(db.JSON)  # JSON object for contact person details
    org_type = db.Column(db.String(50))
    verification_status = db.Column(db.String(20))
    cause_categories = db.Column(ARRAY(db.String(50)))
    notification_preferences = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity': 'organization',
    }

    def __repr__(self):
        return f'<Organization {self.org_name}>'
