from flask import Blueprint, request, jsonify, current_app
from services.user_service import UserService
from dotenv import load_dotenv

auth_blueprint = Blueprint('auth', __name__)


def token_required(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid Authorization header"}), 401
        token = auth_header.split()[1]
        
        user_service: UserService = current_app.config['USER_SERVICE']
        username = user_service.validate_token(token)
        if not username:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    user_service: UserService = current_app.config['USER_SERVICE']
    user = user_service.register(username, password)
    if user:
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"message": "User already exists"}), 400


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_service: UserService = current_app.config['USER_SERVICE']
    token = user_service.login(username, password)
    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401