from flask import Blueprint, request
from src.services.auth_service import AuthService
from src.utils.responses import success_response, error_response

# Blueprint - modular way to organize routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User Signup Endpoint
    
    Request Body (JSON):
    {
        "username": "john",
        "email": "john@example.com",
        "password": "pass123"
    }
    
    Response:
    {
        "success": true,
        "message": "User registered successfully",
        "data": {
            "user": {...},
            "access_token": "...",
            "refresh_token": "..."
        }
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return error_response("No data provided", 400)
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return error_response("Username, email, and password are required", 400)
        
        # Call service to handle business logic
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
    """
    User Login Endpoint
    
    Request Body (JSON):
    {
        "username": "john",
        "password": "pass123"
    }
    
    Response:
    {
        "success": true,
        "message": "Login successful",
        "data": {
            "user": {...},
            "access_token": "...",
            "refresh_token": "..."
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("No data provided", 400)
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return error_response("Username and password are required", 400)
        
        # Call service to handle authentication
        result, error = AuthService.login(username, password)
        
        if error:
            return error_response(error, 401)
        
        return success_response(
            data=result,
            message="Login successful"
        )
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)