from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """
    Standardized success response
    
    Why?
    - Consistent response format across all endpoints
    - Frontend knows what to expect
    """
    response = {
        'success': True,
        'message': message
    }
    if data:
        response['data'] = data
    
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    """
    Standardized error response
    
    Status codes:
    - 400: Bad Request (validation errors)
    - 401: Unauthorized (not logged in)
    - 403: Forbidden (no permission)
    - 404: Not Found
    - 500: Internal Server Error
    """
    response = {
        'success': False,
        'message': message
    }
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code