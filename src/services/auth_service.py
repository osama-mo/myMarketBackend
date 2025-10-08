from src.database import bcrypt
from src.repositories.user_repository import UserRepository
from src.utils.validators import validate_username, validate_email_format, validate_password
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:
    """
    Authentication Service - Business logic for signup/login
    """
    
    @staticmethod
    def signup(username, email, password):
        """Register a new user"""
        
        # Validate username
        is_valid, error = validate_username(username)
        if not is_valid:
            return None, error
        
        # Validate email
        is_valid, error = validate_email_format(email)
        if not is_valid:
            return None, error
        
        # Validate password
        is_valid, error = validate_password(password)
        if not is_valid:
            return None, error
        
        # Check if user already exists
        if UserRepository.user_exists(username=username):
            return None, "Username already exists"
        
        if UserRepository.user_exists(email=email):
            return None, "Email already exists"
        
        # Hash password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create user
        user = UserRepository.create_user(username, email, password_hash)
        
        # Generate JWT tokens with STRING identity (not integer!)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }, None
    
    @staticmethod
    def login(username, password):
        """Login existing user"""
        
        # Find user
        user = UserRepository.get_user_by_username(username)
        if not user:
            return None, "Invalid username or password"
        
        # Check password
        if not bcrypt.check_password_hash(user.password_hash, password):
            return None, "Invalid username or password"
        
        # Generate tokens with STRING identity
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }, None