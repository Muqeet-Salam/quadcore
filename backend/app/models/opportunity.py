from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(ARRAY(db.String(50)))
    duration_type = db.Column(db.String(20))  # 'one-time' or 'ongoing'
    opportunity_type = db.Column(db.String(20))  # 'in-person' or 'remote'
    location = db.Column(db.String(100))
    min_volunteers = db.Column(db.Integer)
    max_volunteers = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    organization = db.relationship('Organization', backref='opportunities')

    def __repr__(self):
        return f'<Opportunity {self.title}>'
