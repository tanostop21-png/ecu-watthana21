"""
Remapping Profile API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_required import jwt_required, get_jwt_identity
from models.remapping_profile import RemappingProfile
from models.vehicle import Vehicle
from models.user import User
from database import db
import logging
import uuid

logger = logging.getLogger(__name__)
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('', methods=['POST'])
@jwt_required()
def create_profile():
    """Create remapping profile"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        vehicle_id = data.get('vehicle_id')
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        profile = RemappingProfile(
            vehicle_id=vehicle_id,
            profile_id=f"PROF_{uuid.uuid4().hex[:12].upper()}",
            profile_name=data.get('profile_name'),
            description=data.get('description'),
            performance_level=data.get('performance_level', 'standard'),
            ecu_parameters=data.get('ecu_parameters', {}),
            transmission_settings=data.get('transmission_settings', {}),
            expected_power_gain=data.get('expected_power_gain'),
            expected_torque_gain=data.get('expected_torque_gain'),
            fuel_consumption_change=data.get('fuel_consumption_change')
        )
        
        db.session.add(profile)
        db.session.commit()
        
        logger.info(f"Profile created: {profile.profile_id}")
        
        return jsonify({
            "status": "success",
            "message": "Profile created",
            "profile": profile.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Create profile error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@profile_bp.route('/vehicle/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def list_profiles(vehicle_id):
    """List profiles for vehicle"""
    try:
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        profiles = RemappingProfile.query.filter_by(vehicle_id=vehicle_id).all()
        
        return jsonify({
            "status": "success",
            "count": len(profiles),
            "profiles": [p.to_dict() for p in profiles]
        }), 200
        
    except Exception as e:
        logger.error(f"List profiles error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@profile_bp.route('/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_profile(profile_id):
    """Get profile details"""
    try:
        user_id = get_jwt_identity()
        
        profile = RemappingProfile.query.join(Vehicle).filter(
            RemappingProfile.id == profile_id,
            Vehicle.user_id == user_id
        ).first()
        
        if not profile:
            return jsonify({"error": "Profile not found"}), 404
        
        return jsonify({
            "status": "success",
            "profile": profile.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@profile_bp.route('/<int:profile_id>', methods=['PUT'])
@jwt_required()
def update_profile(profile_id):
    """Update profile"""
    try:
        user_id = get_jwt_identity()
        
        profile = RemappingProfile.query.join(Vehicle).filter(
            RemappingProfile.id == profile_id,
            Vehicle.user_id == user_id
        ).first()
        
        if not profile:
            return jsonify({"error": "Profile not found"}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'profile_name' in data:
            profile.profile_name = data['profile_name']
        if 'description' in data:
            profile.description = data['description']
        if 'performance_level' in data:
            profile.performance_level = data['performance_level']
        if 'ecu_parameters' in data:
            profile.ecu_parameters = data['ecu_parameters']
        if 'transmission_settings' in data:
            profile.transmission_settings = data['transmission_settings']
        if 'expected_power_gain' in data:
            profile.expected_power_gain = data['expected_power_gain']
        if 'expected_torque_gain' in data:
            profile.expected_torque_gain = data['expected_torque_gain']
        
        db.session.commit()
        
        logger.info(f"Profile updated: {profile.profile_id}")
        
        return jsonify({
            "status": "success",
            "message": "Profile updated",
            "profile": profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@profile_bp.route('/<int:profile_id>/activate', methods=['POST'])
@jwt_required()
def activate_profile(profile_id):
    """Activate profile on vehicle"""
    try:
        user_id = get_jwt_identity()
        
        profile = RemappingProfile.query.join(Vehicle).filter(
            RemappingProfile.id == profile_id,
            Vehicle.user_id == user_id
        ).first()
        
        if not profile:
            return jsonify({"error": "Profile not found"}), 404
        
        # Deactivate other profiles
        RemappingProfile.query.filter_by(vehicle_id=profile.vehicle_id).update({'is_active': False})
        
        # Activate this profile
        profile.is_active = True
        profile.vehicle.current_profile = profile.performance_level
        
        db.session.commit()
        
        logger.info(f"Profile activated: {profile.profile_id}")
        
        return jsonify({
            "status": "success",
            "message": "Profile activated",
            "profile": profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Activate profile error: {str(e)}")
        return jsonify({"error": str(e)}), 500
