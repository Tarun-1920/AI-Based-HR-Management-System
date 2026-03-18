from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from database import db_instance
import traceback

# Initialize Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

# Enable CORS for React frontend with comprehensive settings
CORS(app, 
     resources={r"/api/*": {
         "origins": "*",
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
         "allow_headers": "*",
         "expose_headers": ["Content-Type", "Authorization"],
         "max_age": 3600
     }})

# Initialize MongoDB connection
db = db_instance.get_db()

# Import and register blueprints
from routes.auth_routes import auth_bp
from routes.job_routes import job_bp
from routes.resume_routes import resume_bp
from routes.candidate_routes import candidate_bp
from routes.communication_routes import communication_bp
from routes.employee_routes import employee_bp
from routes.chatbot_routes import chatbot_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(job_bp, url_prefix='/api/jobs')
app.register_blueprint(resume_bp, url_prefix='/api/resumes')
app.register_blueprint(candidate_bp, url_prefix='/api/candidates')
app.register_blueprint(communication_bp, url_prefix='/api/communications')
app.register_blueprint(employee_bp, url_prefix='/api/employees')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

# Root endpoint
@app.route('/')
def home():
    return jsonify({
        'message': 'AI-Based HR Management System API',
        'version': '1.0',
        'database': Config.DATABASE_NAME,
        'endpoints': {
            'auth': '/api/auth',
            'jobs': '/api/jobs',
            'resumes': '/api/resumes',
            'candidates': '/api/candidates'
        }
    }), 200

# Health check endpoint
@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'}), 200

# Database stats endpoint
@app.route('/api/stats')
def stats():
    db_stats = db_instance.get_stats()
    return jsonify(db_stats), 200

# Test database connection endpoint
@app.route('/api/test-db', methods=['GET'])
def test_db():
    try:
        test_collection = db['test_connection']
        from datetime import datetime
        test_record = {'message': 'MongoDB connection successful', 'timestamp': datetime.utcnow().isoformat()}
        result = test_collection.insert_one(test_record)
        test_collection.delete_many({})
        return jsonify({'success': True, 'message': 'MongoDB connection verified successfully', 'inserted_id': str(result.inserted_id)}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'MongoDB connection failed: {str(e)}'}), 500

# Request logging middleware
@app.before_request
def log_request():
    if request.method != 'OPTIONS':
        print(f"\n{'='*60}")
        print(f"Request: {request.method} {request.path}")
        print(f"Origin: {request.headers.get('Origin', 'N/A')}")
        if request.is_json:
            print(f"Body: {request.get_json()}")
        print(f"{'='*60}\n")

# Response headers middleware
@app.after_request
def after_request(response):
    # Add CORS headers to all responses
    origin = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Max-Age'] = '3600'
    
    return response

# Error handlers with standardized JSON responses
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'message': 'Bad Request',
        'error': str(error)
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'message': 'Unauthorized',
        'error': 'Authentication required'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'message': 'Forbidden',
        'error': 'Access denied'
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Not Found',
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'Method Not Allowed',
        'error': f'Method {request.method} not allowed for this endpoint'
    }), 405

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'success': False,
        'message': 'Payload Too Large',
        'error': 'File size exceeds maximum limit'
    }), 413

@app.errorhandler(500)
def internal_error(error):
    print(f"\n{'='*60}")
    print("INTERNAL SERVER ERROR:")
    print(traceback.format_exc())
    print(f"{'='*60}\n")
    return jsonify({
        'success': False,
        'message': 'Internal Server Error',
        'error': 'An unexpected error occurred'
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    print(f"\n{'='*60}")
    print("UNHANDLED EXCEPTION:")
    print(traceback.format_exc())
    print(f"{'='*60}\n")
    return jsonify({
        'success': False,
        'message': 'Server Error',
        'error': str(error)
    }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("AI-Based HR Management System API")
    print("="*60)
    print(f"Server: http://{Config.HOST}:{Config.PORT}")
    print(f"Database: {Config.DATABASE_NAME}")
    print(f"Debug Mode: {Config.DEBUG}")
    print("="*60 + "\n")
    
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
