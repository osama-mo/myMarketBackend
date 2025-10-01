from src.database import db
from datetime import datetime

class User(db.Model):
    """
    User Model - Represents a user in our system
    
    Why these fields?
    - id: Unique identifier (Primary Key)
    - username: Unique login name
    - email: Unique email (for password reset, notifications)
    - password_hash: Encrypted password (NEVER store plain passwords!)
    - created_at: When user registered
    """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<User {self.username}>'
    
    def to_dict(self):
        """
        Convert user object to dictionary
        Used when sending data to frontend (as JSON)
        Notice: We DON'T include password_hash for security!
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }