"""
Main application entry point
"""
import os
from dotenv import load_dotenv
from api import create_app
from config import DevelopmentConfig
from utils.logger import setup_logger

load_dotenv()

logger = setup_logger(__name__)

if __name__ == '__main__':
    # Create Flask app
    app = create_app(DevelopmentConfig)
    
    # Get config
    host = app.config.get('API_HOST', '0.0.0.0')
    port = app.config.get('API_PORT', 5000)
    debug = app.config.get('DEBUG', True)
    
    logger.info(f"Starting ECU-Watthana21 Server on {host}:{port}")
    
    # Run server
    app.run(host=host, port=port, debug=debug)
