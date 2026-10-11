from database import db
from datetime import datetime

class SystemConfig(db.Model):
    """System configuration model"""
    __tablename__ = 'system_config'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(200), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # system, email, security, etc.
    is_sensitive = db.Column(db.Boolean, default=False)  # Should not be logged
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_value=False):
        """Convert to dictionary"""
        data = {
            "key": self.key,
            "category": self.category,
            "description": self.description
        }
        if include_value and not self.is_sensitive:
            data["value"] = self.value
        return data
    
    def __repr__(self):
        return f'<SystemConfig {self.key}>'
