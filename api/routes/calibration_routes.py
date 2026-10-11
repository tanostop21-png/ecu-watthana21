"""
Calibration Log API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_required import jwt_required, get_jwt_identity
from models.calibration_log import CalibrationLog
from models.vehicle import Vehicle
from database import db
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
calibration_bp = Blueprint('calibration', __name__, url_prefix='/calibration')


@calibration_bp.route('', methods=['POST'])
@jwt_required()
def log_calibration():
    """Log calibration change"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        vehicle_id = data.get('vehicle_id')
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        log = CalibrationLog(
            vehicle_id=vehicle_id,
            parameter_name=data.get('parameter_name'),
            old_value=data.get('old_value'),
            new_value=data.get('new_value'),
            unit=data.get('unit'),
            change_type=data.get('change_type', 'ecu'),
            description=data.get('description'),
            status=data.get('status', 'success')
        )
        
        db.session.add(log)
        db.session.commit()
        
        logger.info(f"Calibration logged: {log.parameter_name}")
        
        return jsonify({
            "status": "success",
            "message": "Calibration logged",
            "log": log.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Log calibration error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@calibration_bp.route('/vehicle/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def get_vehicle_logs(vehicle_id):
    """Get calibration logs for vehicle"""
    try:
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        # Get logs from last 30 days by default
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        logs = CalibrationLog.query.filter_by(vehicle_id=vehicle_id).filter(
            CalibrationLog.created_at >= start_date
        ).order_by(CalibrationLog.created_at.desc()).all()
        
        return jsonify({
            "status": "success",
            "count": len(logs),
            "logs": [l.to_dict() for l in logs]
        }), 200
        
    except Exception as e:
        logger.error(f"Get logs error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@calibration_bp.route('/vehicle/<int:vehicle_id>/summary', methods=['GET'])
@jwt_required()
def get_logs_summary(vehicle_id):
    """Get calibration logs summary"""
    try:
        user_id = get_jwt_identity()
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        logs = CalibrationLog.query.filter_by(vehicle_id=vehicle_id).filter(
            CalibrationLog.created_at >= start_date
        ).all()
        
        # Count by type and status
        summary = {
            "total_changes": len(logs),
            "successful": len([l for l in logs if l.status == 'success']),
            "failed": len([l for l in logs if l.status == 'failed']),
            "by_type": {
                "ecu": len([l for l in logs if l.change_type == 'ecu']),
                "transmission": len([l for l in logs if l.change_type == 'transmission']),
                "profile": len([l for l in logs if l.change_type == 'profile'])
            }
        }
        
        return jsonify({
            "status": "success",
            "summary": summary
        }), 200
        
    except Exception as e:
        logger.error(f"Get summary error: {str(e)}")
        return jsonify({"error": str(e)}), 500
