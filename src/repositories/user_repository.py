from src.database import db
from src.models.user import User

class UserRepository:
    """
    Repository Pattern - Handles all database operations for User
    
    Why separate this?
    - Single Responsibility: only deals with database
    - Easy to test
    - Easy to swap database later (SQL to MongoDB)
    """
    
    @staticmethod
    def create_user(username, email, password_hash):
        """Create and save a new user"""
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_username(username):
        """Find user by username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """Find user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Find user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def user_exists(username=None, email=None):
        """Check if user exists by username or email"""
        if username and UserRepository.get_user_by_username(username):
            return True
        if email and UserRepository.get_user_by_email(email):
            return True
        return False