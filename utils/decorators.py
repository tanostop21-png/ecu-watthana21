from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from models.user import User
import logging

logger = logging.getLogger(__name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            logger.warning(f"Unauthorized admin access attempt by user {user_id}")
            return {'error': 'Admin access required'}, 403
        
        return f(*args, **kwargs)
    return decorated_function

def verify_vehicle_ownership(f):
    """Decorator to verify vehicle ownership"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        from models.vehicle import Vehicle
        
        user_id = get_jwt_identity()
        vehicle_id = kwargs.get('vehicle_id')
        
        vehicle = Vehicle.query.filter_by(id=vehicle_id, user_id=user_id).first()
        if not vehicle:
            logger.warning(f"Unauthorized vehicle access by user {user_id}")
            return {'error': 'Vehicle not found or access denied'}, 404
        
        return f(*args, **kwargs)
    return decorated_function

def log_activity(action: str):
    """Decorator to log user activities"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from models.activity_log import ActivityLog
            from database import db
            
            user_id = None
            try:
                user_id = get_jwt_identity()
            except:
                pass
            
            result = f(*args, **kwargs)
            
            if user_id:
                try:
                    log = ActivityLog(
                        user_id=user_id,
                        action=action,
                        endpoint=request.path,
                        method=request.method,
                        status=result[1] if isinstance(result, tuple) and len(result) > 1 else 200
                    )
                    db.session.add(log)
                    db.session.commit()
                except Exception as e:
                    logger.error(f"Failed to log activity: {str(e)}")
            
            return result
        return decorated_function
    return decorator
