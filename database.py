"""
Database initialization and connection
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def init_db(app):
    """Initialize database with app"""
    db.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        db.create_all()
