"""
Flask API Application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig
from database import db, bcrypt, init_db
from utils.logger import setup_logger
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)

def create_app(config=None):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = DevelopmentConfig
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Initialize database
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from api.routes import (
        auth_bp, vehicle_bp, profile_bp, 
        calibration_bp, session_bp, dashboard_bp
    )
    
    app.register_blueprint(auth_bp, url_prefix=f"{app.config['API_PREFIX']}/auth")
    app.register_blueprint(vehicle_bp, url_prefix=f"{app.config['API_PREFIX']}/vehicle")
    app.register_blueprint(profile_bp, url_prefix=f"{app.config['API_PREFIX']}/profile")
    app.register_blueprint(calibration_bp, url_prefix=f"{app.config['API_PREFIX']}/calibration")
    app.register_blueprint(session_bp, url_prefix=f"{app.config['API_PREFIX']}/session")
    app.register_blueprint(dashboard_bp, url_prefix=f"{app.config['API_PREFIX']}/dashboard")
    
    # Root endpoint
    @app.route('/api', methods=['GET'])
    def api_root():
        return jsonify({
            "status": "success",
            "message": "ECU-Watthana21 API",
            "version": "1.0.0",
            "endpoints": {
                "auth": f"{app.config['API_PREFIX']}/auth",
                "vehicle": f"{app.config['API_PREFIX']}/vehicle",
                "profile": f"{app.config['API_PREFIX']}/profile",
                "calibration": f"{app.config['API_PREFIX']}/calibration",
                "session": f"{app.config['API_PREFIX']}/session",
                "dashboard": f"{app.config['API_PREFIX']}/dashboard"
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Server error: {str(error)}")
        return jsonify({"error": "Internal server error"}), 500
    
    logger.info("Flask application created successfully")
    return app
