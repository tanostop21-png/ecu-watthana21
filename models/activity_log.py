from database import db
from datetime import datetime

class ActivityLog(db.Model):
    """Activity log model for tracking user actions"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action = db.Column(db.String(200), nullable=False)  # e.g., 'vehicle_created', 'profile_activated'
    endpoint = db.Column(db.String(500))
    method = db.Column(db.String(10))  # GET, POST, PUT, DELETE
    status = db.Column(db.Integer)  # HTTP status code
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = db.relationship('User', backref='activity_logs')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "action": self.action,
            "endpoint": self.endpoint,
            "method": self.method,
            "status": self.status,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ActivityLog {self.action} by user {self.user_id}>'
