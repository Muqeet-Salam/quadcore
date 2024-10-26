from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.User import User
from app.models.volunteer import Volunteer
from app.models.organization import Organization
from app.models.opportunity import Opportunity
from app.models.volunteer_match import VolunteerMatch
from app.services.recommendation import VolunteerRecommendationSystem
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return "Welcome to VolunMatch!"

@bp.route('/api/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    if current_user.role != 'volunteer':
        return jsonify({"error": "Only volunteers can get recommendations"}), 403

    opportunity_id = request.args.get('opportunity_id', type=int)
    if not opportunity_id:
        return jsonify({"error": "Opportunity ID is required"}), 400

    recommender = VolunteerRecommendationSystem()
    try:
        recommender.fetch_data()
        recommender.preprocess_data()
        recommender.train_content_based_model()
        recommender.train_collaborative_model()

        recommendations = recommender.get_hybrid_recommendations(current_user.id, opportunity_id, top_n=5)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": "Unable to generate recommendations", "details": str(e)}), 500

@bp.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    if current_user.role == 'volunteer':
        user = Volunteer.query.get(current_user.id)
    else:
        user = Organization.query.get(current_user.id)
    return jsonify(user.to_dict())

@bp.route('/api/opportunities', methods=['GET'])
def get_opportunities():
    opportunities = Opportunity.query.all()
    return jsonify([opp.to_dict() for opp in opportunities])

@bp.route('/api/opportunity', methods=['POST'])
@login_required
def create_opportunity():
    if current_user.role != 'organization':
        return jsonify({"error": "Only organizations can create opportunities"}), 403
    
    data = request.json
    new_opportunity = Opportunity(
        organization_id=current_user.id,
        title=data['title'],
        description=data['description'],
        required_skills=data.get('required_skills', []),
        location=data.get('location', ''),
        duration_type=data.get('duration_type', ''),
        opportunity_type=data.get('opportunity_type', ''),
        min_volunteers=data.get('min_volunteers'),
        max_volunteers=data.get('max_volunteers'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date')
    )
    db.session.add(new_opportunity)
    db.session.commit()
    return jsonify(new_opportunity.to_dict()), 201

@bp.route('/api/volunteer_rating', methods=['POST'])
@login_required
def update_volunteer_rating():
    if current_user.role != 'organization':
        return jsonify({"error": "Only organizations can rate volunteers"}), 403

    data = request.json
    volunteer_match = VolunteerMatch.query.get(data['match_id'])
    
    if not volunteer_match:
        return jsonify({"error": "Volunteer match not found"}), 404

    volunteer_match.volunteer_rating = data['rating']
    volunteer_match.organization_review = data.get('review', '')
    db.session.commit()

    # Update the volunteer's average rating
    volunteer = Volunteer.query.get(volunteer_match.volunteer_id)
    volunteer.update_average_rating()

    return jsonify({"message": "Volunteer rating updated successfully"}), 200

# Add more routes as needed
