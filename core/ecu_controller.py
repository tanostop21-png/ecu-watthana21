"""
ECU Controller - manages ECU operations
"""
import logging
from typing import Dict, Any
from datetime import datetime
from models.calibration_log import CalibrationLog
from database import db

logger = logging.getLogger(__name__)

class ECUController:
    """ECU Controller for engine parameter management"""
    
    def __init__(self, vehicle_id: int):
        self.vehicle_id = vehicle_id
        self.is_connected = False
    
    def connect(self) -> bool:
        """Connect to ECU"""
        try:
            logger.info(f"Connecting to ECU for vehicle: {self.vehicle_id}")
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to ECU: {str(e)}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from ECU"""
        try:
            logger.info(f"Disconnecting from ECU for vehicle: {self.vehicle_id}")
            self.is_connected = False
            return True
        except Exception as e:
            logger.error(f"Failed to disconnect: {str(e)}")
            return False
    
    def write_parameter(self, param_name: str, value: float, old_value: float = None) -> bool:
        """Write parameter to ECU"""
        if not self.is_connected:
            logger.warning("ECU not connected")
            return False
        
        try:
            # Log the change
            log = CalibrationLog(
                vehicle_id=self.vehicle_id,
                parameter_name=param_name,
                old_value=old_value,
                new_value=value,
                change_type='ecu',
                status='success'
            )
            db.session.add(log)
            db.session.commit()
            
            logger.info(f"Parameter '{param_name}' written: {old_value} -> {value}")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to write parameter: {str(e)}")
            return False
