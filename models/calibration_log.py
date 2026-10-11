"""
Calibration Log model for tracking changes
"""
from database import db
from datetime import datetime

class CalibrationLog(db.Model):
    """Log all calibration and parameter changes"""
    __tablename__ = 'calibration_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    parameter_name = db.Column(db.String(120), nullable=False)
    old_value = db.Column(db.Float)
    new_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50))
    change_type = db.Column(db.String(50), nullable=False)  # ecu, transmission, profile
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='success')  # success, failed, pending
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "parameter_name": self.parameter_name,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "unit": self.unit,
            "change_type": self.change_type,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<CalibrationLog {self.parameter_name}: {self.old_value} -> {self.new_value}>'
