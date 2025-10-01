import re
from email_validator import validate_email, EmailNotValidError

def validate_username(username):
    """
    Validate username
    Rules:
    - 3-80 characters
    - Only letters, numbers, underscore
    """
    if not username or len(username) < 3 or len(username) > 80:
        return False, "Username must be between 3 and 80 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, None

def validate_email_format(email):
    """Validate email format using email-validator library"""
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def validate_password(password):
    """
    Validate password strength
    Rules:
    - At least 6 characters
    - Contains letter and number
    """
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
        return False, "Password must contain both letters and numbers"
    
    return True, None