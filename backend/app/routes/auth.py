from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from app.models.User import User
from app.models.volunteer import Volunteer
from app.models.organization import Organization
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({"message": "Logged in successfully", "user": user.to_dict()}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@auth.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered"}), 400
    
    if data['role'] == 'volunteer':
        new_user = Volunteer(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            # Add other Volunteer-specific fields
        )
    elif data['role'] == 'organization':
        new_user = Organization(
            email=data['email'],
            org_name=data['org_name'],
            # Add other Organization-specific fields
        )
    else:
        return jsonify({"message": "Invalid role"}), 400
    
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
    return jsonify({"message": "Registered successfully", "user": new_user.to_dict()}), 201

# Add other auth-related routes here (e.g., register, logout)
