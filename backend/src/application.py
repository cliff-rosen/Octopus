from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, decode_token
from flask_cors import CORS  # Add this import
from functools import wraps
from db.database import Database
from config import DB_CONFIG
import uuid
import logging
from werkzeug.exceptions import UnprocessableEntity

app = Flask(__name__)
# Configure CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "methods": ["GET", "POST", "OPTIONS"]}})

app.config['JWT_SECRET_KEY'] = str(uuid.uuid4())  # Use a secure key in production
jwt = JWTManager(app)

db = Database()

# Set up logging
logging.basicConfig(level=logging.INFO)  # Fixed: Closed parenthesis
logger = logging.getLogger(__name__)

# Add this decorator function
def add_cors_headers(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    return wrapper

# Custom decorator to check JWT in request body
def jwt_required_in_body(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.json.get('token')
        if not token:
            logger.error("No token provided in request body")
            return jsonify({"msg": "Missing token in request body"}), 401
        try:
            decoded_token = decode_token(token)
            identity = decoded_token['sub']
            return fn(identity, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error verifying JWT: {str(e)}. Token: {token}")
            return jsonify({"msg": f"JWT verification failed. Token: {token}"}), 401
    return wrapper

@app.errorhandler(UnprocessableEntity)
def handle_unprocessable_entity(e):
    logger.error(f"Unprocessable Entity: {str(e)}")
    return jsonify({"msg": "Unprocessable Entity", "errors": e.data['messages']}), 422

@app.errorhandler(401)
def unauthorized(error):
    headers = dict(request.headers)
    logger.error(f"Unauthorized access attempt. Headers: {headers}")
    return jsonify({"msg": error.description, "headers": headers}), 401

# Add this new route for user registration
@app.route('/auth/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    
    existing_user = db.execute("SELECT id FROM users WHERE username = %s", (username,))
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 409
    
    user_id = db.create_user(username, password)
    if user_id:
        return jsonify({"msg": "User registered successfully", "user_id": user_id}), 201
    else:
        return jsonify({"msg": "Registration failed"}), 500

@app.route('/auth/login', methods=['POST'])
@add_cors_headers
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        logger.error(f"Login attempt failed: Missing username or password")
        return jsonify({"msg": "Missing username or password"}), 400
    
    try:
        user_id = db.authenticate_user(username, password)
        if user_id:
            access_token = create_access_token(identity=user_id)
            logger.info(f"User {username} logged in successfully")
            logger.info(f"Bearer token created: {access_token}")
            return jsonify(access_token=access_token), 200
        else:
            logger.warning(f"Login attempt failed for user {username}: Invalid credentials")
            return jsonify({"msg": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Login attempt failed for user {username}: {str(e)}")
        return jsonify({"msg": "An error occurred during login"}), 500

@app.route('/auth/logout', methods=['POST'])
@jwt_required_in_body
def logout(identity):
    # In a real application, you might want to invalidate the token here
    return jsonify({"msg": "Logout successful"}), 200

@app.route('/screens', methods=['POST'])
@jwt_required_in_body
def get_screens(identity):
    screens = db.get_user_screens(identity)
    # Add width and height to each screen
    for screen in screens:
        screen['width'] = 800
        screen['height'] = 500
    return jsonify(screens), 200

@app.route('/screens/create', methods=['POST'])
@jwt_required_in_body
def create_screen(identity):
    name = request.json.get('name', None)
    content = request.json.get('content', '')
    if not name:
        return jsonify({"msg": "Screen name is required"}), 400
    try:
        screen = db.create_screen(identity, name, content)
        return jsonify(screen), 201
    except Exception as e:
        logger.error(f"Error creating screen: {str(e)}")
        return jsonify({"msg": "An error occurred while creating the screen"}), 500

@app.route('/screens/get', methods=['POST'])
@jwt_required_in_body
def get_screen(identity):
    screen_id = request.json.get('screen_id')
    if not screen_id:
        return jsonify({"msg": "Screen ID is required"}), 400
    screen = db.get_screen(screen_id, identity)
    if screen:
        return jsonify(screen), 200
    else:
        return jsonify({"msg": "Screen not found or access denied"}), 404

@app.route('/screens/update', methods=['POST'])
@jwt_required_in_body
def update_screen(identity):
    screen_id = request.json.get('screen_id')
    name = request.json.get('name')
    content = request.json.get('content')
    if not screen_id:
        return jsonify({"msg": "Screen ID is required"}), 400
    if name is None and content is None:
        return jsonify({"msg": "Name or content is required"}), 400
    screen = db.update_screen(screen_id, identity, name=name, content=content)
    if screen:
        return jsonify(screen), 200
    else:
        return jsonify({"msg": "Screen not found or access denied"}), 404

@app.route('/screens/delete', methods=['POST'])
@jwt_required_in_body
def delete_screen(identity):
    screen_id = request.json.get('screen_id')
    if not screen_id:
        return jsonify({"msg": "Screen ID is required"}), 400
    db.delete_screen(screen_id, identity)
    return jsonify({"msg": "Screen deleted"}), 200

@app.route('/screens/content/get', methods=['POST'])
@jwt_required_in_body
def get_screen_content(identity):
    screen_id = request.json.get('screen_id')
    if not screen_id:
        return jsonify({"msg": "Screen ID is required"}), 400
    content = db.get_screen_content(screen_id, identity)
    if content is not None:
        return jsonify({"content": content}), 200
    else:
        return jsonify({"msg": "Screen not found or access denied"}), 404

@app.route('/screens/content/update', methods=['POST'])
@jwt_required_in_body
def update_screen_content(identity):
    screen_id = request.json.get('screen_id')
    content = request.json.get('content')
    if not screen_id:
        return jsonify({"msg": "Screen ID is required"}), 400
    if content is None:
        return jsonify({"msg": "Content is required"}), 400
    screen = db.update_screen_content(screen_id, identity, content)
    if screen:
        return jsonify(screen), 200
    else:
        return jsonify({"msg": "Screen not found or access denied"}), 404

@app.route('/screens/clear', methods=['POST'])
@jwt_required_in_body
def clear_all_screens(identity):
    try:
        deleted_count = db.clear_user_screens(identity)
        if deleted_count > 0:
            return jsonify({"msg": f"Successfully deleted {deleted_count} screens"}), 200
        else:
            return jsonify({"msg": "No screens found for the user"}), 404
    except Exception as e:
        logger.error(f"Error clearing screens: {str(e)}")
        return jsonify({"msg": "An error occurred while clearing screens"}), 500

if __name__ == '__main__':
    app.run(debug=True)