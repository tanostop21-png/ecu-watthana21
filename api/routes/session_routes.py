"""
Tuning Session API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.tuning_session import TuningSession
from models.vehicle import Vehicle
from database import db
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)
session_bp = Blueprint('session', __name__, url_prefix='/session')


@session_bp.route('', methods=['POST'])
@jwt_required()
def create_session():
    """Create tuning session"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        vehicle_id = data.get('vehicle_id')
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        session = TuningSession(
            session_id=f"TSN_{uuid.uuid4().hex[:12].upper()}",
            vehicle_id=vehicle_id,
            profile_id=data.get('profile_id'),
            technician_id=user_id,
            session_name=data.get('session_name'),
            description=data.get('description'),
            before_hp=data.get('before_hp'),
            before_torque=data.get('before_torque')
        )
        
        db.session.add(session)
        db.session.commit()
        
        logger.info(f"Tuning session created: {session.session_id}")
        
        return jsonify({
            "status": "success",
            "message": "Session created",
            "session": session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Create session error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@session_bp.route('/vehicle/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def list_sessions(vehicle_id):
    """List tuning sessions for vehicle"""
    try:
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        sessions = TuningSession.query.filter_by(vehicle_id=vehicle_id).order_by(
            TuningSession.created_at.desc()
        ).all()
        
        return jsonify({
            "status": "success",
            "count": len(sessions),
            "sessions": [s.to_dict() for s in sessions]
        }), 200
        
    except Exception as e:
        logger.error(f"List sessions error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@session_bp.route('/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    """Get session details"""
    try:
        user_id = get_jwt_identity()
        
        session = TuningSession.query.join(Vehicle).filter(
            TuningSession.id == session_id,
            Vehicle.user_id == user_id
        ).first()
        
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        return jsonify({
            "status": "success",
            "session": session.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Get session error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@session_bp.route('/<int:session_id>', methods=['PUT'])
@jwt_required()
def update_session(session_id):
    """Update session"""
    try:
        user_id = get_jwt_identity()
        
        session = TuningSession.query.join(Vehicle).filter(
            TuningSession.id == session_id,
            Vehicle.user_id == user_id
        ).first()
        
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            session.status = data['status']
        if 'progress_percentage' in data:
            session.progress_percentage = data['progress_percentage']
        if 'total_changes' in data:
            session.total_changes = data['total_changes']
        if 'successful_changes' in data:
            session.successful_changes = data['successful_changes']
        if 'failed_changes' in data:
            session.failed_changes = data['failed_changes']
        if 'after_hp' in data:
            session.after_hp = data['after_hp']
        if 'after_torque' in data:
            session.after_torque = data['after_torque']
        
        if data.get('status') == 'completed':
            session.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Session updated: {session.session_id}")
        
        return jsonify({
            "status": "success",
            "message": "Session updated",
            "session": session.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update session error: {str(e)}")
        return jsonify({"error": str(e)}), 500
