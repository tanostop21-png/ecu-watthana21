"""
API Routes initialization
"""
from .auth_routes import auth_bp
from .vehicle_routes import vehicle_bp
from .profile_routes import profile_bp
from .calibration_routes import calibration_bp
from .session_routes import session_bp
from .dashboard_routes import dashboard_bp

__all__ = ['auth_bp', 'vehicle_bp', 'profile_bp', 'calibration_bp', 'session_bp', 'dashboard_bp']
