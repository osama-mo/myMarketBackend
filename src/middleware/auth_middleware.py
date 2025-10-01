from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from src.repositories.user_repository import UserRepository
from src.utils.responses import error_response

def jwt_required_custom(fn):
    """
    Custom JWT decorator that also fetches user from database
    
    Why?
    - Verifies JWT token is valid
    - Gets user ID from token
    - Fetches full user object from database
    - Makes user available to route function
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT token exists and is valid
            verify_jwt_in_request()
            
            # Get user ID from token payload
            user_id = get_jwt_identity()
            
            # Fetch user from database
            user = UserRepository.get_user_by_id(user_id)
            
            if not user:
                return error_response("User not found", 404)
            
            # Pass user to the route function
            return fn(current_user=user, *args, **kwargs)
            
        except Exception as e:
            return error_response(f"Authentication failed: {str(e)}", 401)
    
    return wrapper