"""
Admin Dashboard API routes
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.vehicle import Vehicle
from models.calibration_log import CalibrationLog
from models.tuning_session import TuningSession
from database import db
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Check if user is admin
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        
        # Get statistics
        total_users = User.query.count()
        total_vehicles = Vehicle.query.count()
        total_sessions = TuningSession.query.count()
        
        # Get recent changes
        today = datetime.utcnow().date()
        changes_today = CalibrationLog.query.filter(
            db.func.date(CalibrationLog.created_at) == today
        ).count()
        
        # Get session status distribution
        session_stats = db.session.query(
            TuningSession.status,
            db.func.count(TuningSession.id)
        ).group_by(TuningSession.status).all()
        
        status_dist = {status: count for status, count in session_stats}
        
        return jsonify({
            "status": "success",
            "stats": {
                "total_users": total_users,
                "total_vehicles": total_vehicles,
                "total_sessions": total_sessions,
                "changes_today": changes_today,
                "session_status_distribution": status_dist
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Dashboard stats error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route('/users', methods=['GET'])
@jwt_required()
def list_all_users():
    """List all users (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        
        users = User.query.all()
        
        return jsonify({
            "status": "success",
            "count": len(users),
            "users": [u.to_dict(include_email=True) for u in users]
        }), 200
        
    except Exception as e:
        logger.error(f"List users error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route('/vehicles', methods=['GET'])
@jwt_required()
def list_all_vehicles():
    """List all vehicles (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        
        vehicles = Vehicle.query.all()
        
        return jsonify({
            "status": "success",
            "count": len(vehicles),
            "vehicles": [v.to_dict() for v in vehicles]
        }), 200
        
    except Exception as e:
        logger.error(f"List vehicles error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route('/sessions', methods=['GET'])
@jwt_required()
def list_all_sessions():
    """List all tuning sessions (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        
        sessions = TuningSession.query.order_by(TuningSession.created_at.desc()).all()
        
        return jsonify({
            "status": "success",
            "count": len(sessions),
            "sessions": [s.to_dict() for s in sessions]
        }), 200
        
    except Exception as e:
        logger.error(f"List sessions error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_calibration_logs():
    """Get calibration logs (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        
        days = 7  # Default last 7 days
        start_date = datetime.utcnow() - timedelta(days=days)
        
        logs = CalibrationLog.query.filter(
            CalibrationLog.created_at >= start_date
        ).order_by(CalibrationLog.created_at.desc()).limit(100).all()
        
        return jsonify({
            "status": "success",
            "count": len(logs),
            "logs": [l.to_dict() for l in logs]
        }), 200
        
    except Exception as e:
        logger.error(f"Get logs error: {str(e)}")
        return jsonify({"error": str(e)}), 500
