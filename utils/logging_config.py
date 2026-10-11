import os
import logging
import logging.handlers
from pathlib import Path
from config import Config

def setup_logging():
    """Setup comprehensive logging system"""
    # Create logs directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
    
    # File handler with rotation
    log_file = log_dir / 'app.log'
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=Config.LOG_MAX_SIZE,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to root logger
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    
    # Error log file
    error_log_file = log_dir / 'error.log'
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=Config.LOG_MAX_SIZE,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    root_logger.addHandler(error_handler)
    
    return root_logger

def get_logger(name):
    """Get logger for module"""
    return logging.getLogger(name)
