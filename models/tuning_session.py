"""
Tuning Session model for tracking tuning work
"""
from database import db
from datetime import datetime

class TuningSession(db.Model):
    """Track tuning sessions and changes"""
    __tablename__ = 'tuning_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('remapping_profiles.id'))
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    session_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Session Status
    status = db.Column(db.String(50), default='draft')  # draft, in_progress, completed, failed
    progress_percentage = db.Column(db.Integer, default=0)
    
    # Changes Summary
    total_changes = db.Column(db.Integer, default=0)
    successful_changes = db.Column(db.Integer, default=0)
    failed_changes = db.Column(db.Integer, default=0)
    
    # Performance Results
    before_hp = db.Column(db.Float)
    after_hp = db.Column(db.Float)
    before_torque = db.Column(db.Float)
    after_torque = db.Column(db.Float)
    
    # Timing
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "session_name": self.session_name,
            "description": self.description,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "total_changes": self.total_changes,
            "successful_changes": self.successful_changes,
            "failed_changes": self.failed_changes,
            "before_hp": self.before_hp,
            "after_hp": self.after_hp,
            "before_torque": self.before_torque,
            "after_torque": self.after_torque,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<TuningSession {self.session_name}>'
