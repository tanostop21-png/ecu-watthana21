"""
Vehicle data model
"""
from database import db
from datetime import datetime

class Vehicle(db.Model):
    """Vehicle information model"""
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    make = db.Column(db.String(80), nullable=False)  # Toyota, Honda, BMW
    model = db.Column(db.String(80), nullable=False)  # Camry, Civic, M340i
    year = db.Column(db.Integer, nullable=False)
    engine_type = db.Column(db.String(50), nullable=False)  # petrol, diesel, hybrid, electric
    transmission_type = db.Column(db.String(50), nullable=False)  # manual, automatic, cvt, dct
    vin = db.Column(db.String(17), unique=True, nullable=False)
    license_plate = db.Column(db.String(20), nullable=True)
    engine_displacement = db.Column(db.Float)  # in cc
    horsepower = db.Column(db.Float)  # stock hp
    torque = db.Column(db.Float)  # in Nm
    current_profile = db.Column(db.String(50), default='stock')
    is_connected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tuning_sessions = db.relationship('TuningSession', backref='vehicle', lazy=True, cascade='all, delete-orphan')
    remapping_profiles = db.relationship('RemappingProfile', backref='vehicle', lazy=True, cascade='all, delete-orphan')
    calibration_logs = db.relationship('CalibrationLog', backref='vehicle', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "engine_type": self.engine_type,
            "transmission_type": self.transmission_type,
            "vin": self.vin,
            "license_plate": self.license_plate,
            "engine_displacement": self.engine_displacement,
            "horsepower": self.horsepower,
            "torque": self.torque,
            "current_profile": self.current_profile,
            "is_connected": self.is_connected,
            "created_at": self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Vehicle {self.year} {self.make} {self.model}>'
