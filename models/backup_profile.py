from database import db
from datetime import datetime
import json

class BackupProfile(db.Model):
    """Backup profile for version control"""
    __tablename__ = 'backup_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('remapping_profiles.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    version = db.Column(db.Integer, nullable=False)  # Version number
    snapshot = db.Column(db.JSON)  # Profile snapshot
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('RemappingProfile', backref='backups')
    vehicle = db.relationship('Vehicle', backref='profile_backups')
    user = db.relationship('User', backref='profile_backups')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "version": self.version,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<BackupProfile Profile {self.profile_id} v{self.version}>'
