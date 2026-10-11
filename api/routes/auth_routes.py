"""
Authentication routes - Login, Register, Token
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from database import db
from utils.validators import validate_email, validate_password
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields"}), 400
        
        if not validate_email(data['email']):
            return jsonify({"error": "Invalid email format"}), 400
        
        if not validate_password(data['password']):
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already registered"}), 409
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            phone=data.get('phone', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"New user registered: {user.username}")
        
        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "user": user.to_dict(include_email=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({"error": "Missing username or password"}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Invalid username or password"}), 401
        
        if not user.is_active:
            return jsonify({"error": "Account is inactive"}), 403
        
        access_token = create_access_token(identity=user.id)
        
        logger.info(f"User logged in: {user.username}")
        
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "status": "success",
            "user": user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        logger.error(f"Profile error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        
        db.session.commit()
        
        logger.info(f"User profile updated: {user.username}")
        
        return jsonify({
            "status": "success",
            "message": "Profile updated",
            "user": user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({"error": "Missing password fields"}), 400
        
        if not user.check_password(data['old_password']):
            return jsonify({"error": "Old password is incorrect"}), 401
        
        if not validate_password(data['new_password']):
            return jsonify({"error": "New password must be at least 8 characters"}), 400
        
        user.set_password(data['new_password'])
        db.session.commit()
        
        logger.info(f"Password changed: {user.username}")
        
        return jsonify({
            "status": "success",
            "message": "Password changed successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Change password error: {str(e)}")
        return jsonify({"error": str(e)}), 500
