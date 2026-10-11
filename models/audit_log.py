from database import db
from datetime import datetime

class AuditLog(db.Model):
    """Audit log for compliance and security"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(200), nullable=False)  # create, update, delete, etc.
    entity_type = db.Column(db.String(50), nullable=False)  # user, vehicle, profile, etc.
    entity_id = db.Column(db.Integer)
    changes = db.Column(db.JSON)  # Before/after changes
    reason = db.Column(db.Text)  # Why the action was taken
    status = db.Column(db.String(50))  # success, failed
    error_message = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = db.relationship('User', backref='audit_logs')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "changes": self.changes,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }
    
    def __repr__(self):
        return f'<AuditLog {self.action} on {self.entity_type} {self.entity_id}>'
