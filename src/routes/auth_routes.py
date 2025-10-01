from flask import Blueprint, request
from src.services.auth_service import AuthService
from src.utils.responses import success_response, error_response
from src.middleware.auth_middleware import jwt_required_custom

# Blueprint - modular way to organize routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User Signup Endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("No data provided", 400)
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return error_response("Username, email, and password are required", 400)
        
        result, error = AuthService.signup(username, email, password)
        
        if error:
            return error_response(error, 400)
        
        return success_response(
            data=result,
            message="User registered successfully",
            status_code=201
        )
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """User Login Endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("No data provided", 400)
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return error_response("Username and password are required", 400)
        
        result, error = AuthService.login(username, password)
        
        if error:
            return error_response(error, 401)
        
        return success_response(
            data=result,
            message="Login successful"
        )
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@auth_bp.route('/me', methods=['GET'])
@jwt_required_custom
def get_current_user(current_user):
    """
    Get Current User Profile (PROTECTED ROUTE)
    
    Requires: Authorization header with Bearer token
    
    Example:
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    
    Response:
    {
        "success": true,
        "message": "User profile retrieved",
        "data": {
            "user": {...}
        }
    }
    """
    try:
        return success_response(
            data={'user': current_user.to_dict()},
            message="User profile retrieved"
        )
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)