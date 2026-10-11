"""
Logging configuration
"""
import logging
import os
from pathlib import Path

def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """Setup logger with file and console handlers"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(log_dir / "app.log")
        fh.setLevel(getattr(logging, log_level))
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, log_level))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger
