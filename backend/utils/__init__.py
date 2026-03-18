import re
from flask import jsonify
from bson import ObjectId

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present in the data.
    
    Args:
        data (dict): The data to validate
        required_fields (list): List of required field names
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not data:
        return False, "Request body is required"
    
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, None

def validate_email(email):
    """
    Validate email format using regex.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_object_id(object_id):
    """
    Validate MongoDB ObjectId format.
    
    Args:
        object_id (str): ObjectId string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not object_id:
        return False
    
    try:
        ObjectId(object_id)
        return True
    except:
        return False

def sanitize_string(value, max_length=None):
    """
    Sanitize string input by stripping whitespace and limiting length.
    
    Args:
        value (str): String to sanitize
        max_length (int, optional): Maximum allowed length
        
    Returns:
        str: Sanitized string
    """
    if not isinstance(value, str):
        value = str(value)
    
    value = value.strip()
    
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    return value

def success_response(message=None, data=None, status_code=200):
    """
    Create a standardized success response.
    
    Args:
        message (str, optional): Success message
        data (dict, optional): Response data
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': True
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def error_response(message, status_code=400):
    """
    Create a standardized error response.
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': False,
        'error': message
    }
    
    return jsonify(response), status_code
