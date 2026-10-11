"""
Configuration settings for ECU Remapping Tool
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Application
    APP_NAME = "ECU-Watthana21"
    APP_VERSION = "1.0.0"
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///ecu_watthana.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-this')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    API_PREFIX = '/api/v1'
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Vehicle Configuration
    VEHICLE_TYPES = {
        "petrol": "Petrol Engine",
        "diesel": "Diesel Engine",
        "hybrid": "Hybrid Engine",
        "electric": "Electric Motor"
    }
    
    # ECU Parameters
    ECU_PARAMS = {
        "fuel_injection_timing": {"min": 0, "max": 100, "unit": "degrees"},
        "boost_pressure": {"min": 0, "max": 3.0, "unit": "bar"},
        "ignition_timing": {"min": -10, "max": 30, "unit": "degrees"},
        "fuel_lambda": {"min": 0.8, "max": 1.2, "unit": "ratio"},
        "intake_valve_timing": {"min": 0, "max": 360, "unit": "degrees"},
        "exhaust_valve_timing": {"min": 0, "max": 360, "unit": "degrees"},
        "max_rpm": {"min": 4000, "max": 10000, "unit": "RPM"},
        "rev_limit": {"min": 5000, "max": 12000, "unit": "RPM"}
    }
    
    # Transmission Settings
    TRANSMISSION_TYPES = {
        "manual": "Manual Transmission",
        "automatic": "Automatic Transmission",
        "cvt": "CVT Transmission",
        "dct": "Dual Clutch Transmission"
    }
    
    # Remapping Profiles
    PROFILE_LEVELS = {
        "stock": {"boost": 0, "fuel_adj": 0, "power_gain": 0},
        "eco": {"boost": -0.2, "fuel_adj": -10, "power_gain": -5},
        "standard": {"boost": 0.2, "fuel_adj": 5, "power_gain": 10},
        "sport": {"boost": 0.8, "fuel_adj": 15, "power_gain": 30},
        "extreme": {"boost": 1.5, "fuel_adj": 25, "power_gain": 50}
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
