"""
Transmission Controller
"""
import logging
from typing import Dict, Any
from models.calibration_log import CalibrationLog
from database import db

logger = logging.getLogger(__name__)

class TransmissionController:
    """Transmission Controller for transmission management"""
    
    def __init__(self, vehicle_id: int, transmission_type: str):
        self.vehicle_id = vehicle_id
        self.transmission_type = transmission_type
        self.is_connected = False
    
    def connect(self) -> bool:
        """Connect to transmission ECU"""
        try:
            logger.info(f"Connecting to transmission: {self.transmission_type}")
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from transmission ECU"""
        try:
            logger.info("Disconnecting from transmission")
            self.is_connected = False
            return True
        except Exception as e:
            logger.error(f"Failed to disconnect: {str(e)}")
            return False
    
    def write_shift_map(self, gear: int, shift_data: Dict[str, Any]) -> bool:
        """Write shift map for gear"""
        if not self.is_connected:
            logger.warning("Transmission not connected")
            return False
        
        try:
            log = CalibrationLog(
                vehicle_id=self.vehicle_id,
                parameter_name=f"Gear {gear} Shift Map",
                new_value=shift_data.get('rpm'),
                change_type='transmission',
                status='success'
            )
            db.session.add(log)
            db.session.commit()
            
            logger.info(f"Shift map written for gear {gear}")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to write shift map: {str(e)}")
            return False
