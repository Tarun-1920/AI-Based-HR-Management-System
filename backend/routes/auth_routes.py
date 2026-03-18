from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from config import Config
from models.user_model import User
from utils import (
    validate_required_fields,
    validate_email,
    success_response,
    error_response,
    sanitize_string
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Required fields: email, password, name
    Optional fields: role (default: 'Candidate')
    
    Returns:
        201: User created successfully
        400: Validation error
        500: Server error
    """
    try:
        data = request.get_json()
        print(f"Registration request received: {data}")  # Debug log
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['email', 'password', 'name'])
        if not is_valid:
            print(f"Validation error: {error_msg}")  # Debug log
            return error_response(error_msg, 400)
        
        # Sanitize inputs
        email = sanitize_string(data['email'].lower(), 255)
        name = sanitize_string(data['name'], 100)
        password = data['password']
        role = sanitize_string(data.get('role', 'Candidate'), 50)
        
        print(f"Sanitized data - Email: {email}, Name: {name}, Role: {role}")  # Debug log
        
        # Validate email format
        if not validate_email(email):
            print(f"Invalid email format: {email}")  # Debug log
            return error_response('Invalid email format', 400)
        
        # Validate password strength
        if len(password) < 6:
            print(f"Password too short: {len(password)} characters")  # Debug log
            return error_response('Password must be at least 6 characters long', 400)
        
        # Validate role
        valid_roles = ['HR', 'Candidate', 'Admin']
        if role not in valid_roles:
            print(f"Invalid role: {role}")  # Debug log
            return error_response(
                f'Invalid role. Must be one of: {", ".join(valid_roles)}',
                400
            )
        
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            print(f"User already exists: {email}")  # Debug log
            return error_response('Email already registered', 409)
        
        # Create new user
        user_id = User.create(email, password, name, role)
        print(f"User created successfully with ID: {user_id}")  # Debug log
        
        return success_response(
            message='User registered successfully',
            data={'user_id': user_id, 'email': email, 'name': name, 'role': role},
            status_code=201
        )
        
    except Exception as e:
        print(f"Registration error: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return error_response(f'Registration failed: {str(e)}', 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    
    Required fields: email, password
    
    Returns:
        200: Login successful with token
        400: Validation error
        401: Invalid credentials
        500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['email', 'password'])
        if not is_valid:
            return error_response(error_msg, 400)
        
        # Sanitize email
        email = sanitize_string(data['email'].lower(), 255)
        password = data['password']
        
        # Validate email format
        if not validate_email(email):
            return error_response('Invalid email format', 400)
        
        # Find user by email
        user = User.find_by_email(email)
        if not user:
            return error_response('Invalid email or password', 401)
        
        # Verify password
        if not User.verify_password(user['password'], password):
            return error_response('Invalid email or password', 401)
        
        # Generate JWT token
        token_payload = {
            'user_id': str(user['_id']),
            'email': user['email'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
        }
        
        token = jwt.encode(token_payload, Config.SECRET_KEY, algorithm='HS256')
        
        # Return success response
        return success_response(
            message='Login successful',
            data={
                'token': token,
                'user': {
                    'id': str(user['_id']),
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            },
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Login failed: {str(e)}', 500)

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """
    Verify JWT token validity.
    
    Requires: Authorization header with Bearer token
    
    Returns:
        200: Token is valid
        401: Token is invalid or expired
    """
    try:
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return error_response('Invalid token format. Use: Bearer <token>', 401)
        
        if not token:
            return error_response('Authentication token is required', 401)
        
        # Decode and verify token
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        
        return success_response(
            message='Token is valid',
            data={
                'user_id': data['user_id'],
                'email': data['email'],
                'role': data['role']
            },
            status_code=200
        )
        
    except jwt.ExpiredSignatureError:
        return error_response('Token has expired', 401)
    except jwt.InvalidTokenError:
        return error_response('Invalid token', 401)
    except Exception as e:
        return error_response(f'Token verification failed: {str(e)}', 401)
