"""
Vehicle API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_required import jwt_required, get_jwt_identity
from models.vehicle import Vehicle
from models.user import User
from database import db
from utils.validators import validate_vehicle
import logging

logger = logging.getLogger(__name__)
vehicle_bp = Blueprint('vehicle', __name__, url_prefix='/vehicle')


@vehicle_bp.route('/register', methods=['POST'])
@jwt_required()
def register_vehicle():
    """Register a new vehicle"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        
        # Validate
        is_valid, message = validate_vehicle(data)
        if not is_valid:
            return jsonify({"error": message}), 400
        
        # Check if vehicle exists
        if Vehicle.query.filter_by(vin=data['vin']).first():
            return jsonify({"error": "Vehicle with this VIN already registered"}), 409
        
        # Create vehicle
        vehicle = Vehicle(
            user_id=user_id,
            vehicle_id=data['vehicle_id'],
            make=data['make'],
            model=data['model'],
            year=data['year'],
            engine_type=data['engine_type'],
            transmission_type=data['transmission_type'],
            vin=data['vin'],
            license_plate=data.get('license_plate'),
            engine_displacement=data.get('engine_displacement'),
            horsepower=data.get('horsepower'),
            torque=data.get('torque')
        )
        
        db.session.add(vehicle)
        db.session.commit()
        
        logger.info(f"Vehicle registered: {vehicle.vehicle_id} by user {user.username}")
        
        return jsonify({
            "status": "success",
            "message": "Vehicle registered successfully",
            "vehicle": vehicle.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Register vehicle error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@vehicle_bp.route('', methods=['GET'])
@jwt_required()
def list_vehicles():
    """List user's vehicles"""
    try:
        user_id = get_jwt_identity()
        
        vehicles = Vehicle.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            "status": "success",
            "count": len(vehicles),
            "vehicles": [v.to_dict() for v in vehicles]
        }), 200
        
    except Exception as e:
        logger.error(f"List vehicles error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@vehicle_bp.route('/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def get_vehicle(vehicle_id):
    """Get vehicle details"""
    try:
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        return jsonify({
            "status": "success",
            "vehicle": vehicle.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Get vehicle error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@vehicle_bp.route('/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    """Update vehicle information"""
    try:
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        data = request.get_json()
        
        # Update fields
        updatable_fields = ['make', 'model', 'license_plate', 'engine_displacement', 'horsepower', 'torque']
        for field in updatable_fields:
            if field in data:
                setattr(vehicle, field, data[field])
        
        db.session.commit()
        
        logger.info(f"Vehicle updated: {vehicle.vehicle_id}")
        
        return jsonify({
            "status": "success",
            "message": "Vehicle updated",
            "vehicle": vehicle.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update vehicle error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@vehicle_bp.route('/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    """Delete vehicle"""
    try:
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        db.session.delete(vehicle)
        db.session.commit()
        
        logger.info(f"Vehicle deleted: {vehicle.vehicle_id}")
        
        return jsonify({
            "status": "success",
            "message": "Vehicle deleted"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete vehicle error: {str(e)}")
        return jsonify({"error": str(e)}), 500
