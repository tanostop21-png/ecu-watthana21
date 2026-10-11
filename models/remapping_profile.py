"""
Remapping Profile data model
"""
from database import db
from datetime import datetime
import json

class RemappingProfile(db.Model):
    """Remapping profile model for storing tuning configurations"""
    __tablename__ = 'remapping_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    profile_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    profile_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    performance_level = db.Column(db.String(50), nullable=False)  # stock, eco, standard, sport, extreme
    
    # ECU Settings (stored as JSON)
    ecu_parameters = db.Column(db.JSON, default={})
    transmission_settings = db.Column(db.JSON, default={})
    
    # Performance Info
    expected_power_gain = db.Column(db.Float)  # in HP
    expected_torque_gain = db.Column(db.Float)  # in Nm
    fuel_consumption_change = db.Column(db.Float)  # in %
    
    is_active = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tuning_sessions = db.relationship('TuningSession', backref='profile', lazy=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "profile_name": self.profile_name,
            "description": self.description,
            "performance_level": self.performance_level,
            "ecu_parameters": self.ecu_parameters,
            "transmission_settings": self.transmission_settings,
            "expected_power_gain": self.expected_power_gain,
            "expected_torque_gain": self.expected_torque_gain,
            "fuel_consumption_change": self.fuel_consumption_change,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<RemappingProfile {self.profile_name}>'
