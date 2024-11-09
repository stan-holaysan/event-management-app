from flask import Blueprint, request, jsonify, make_response
from models import db, User, bcrypt
from flask_jwt_extended import create_access_token
# from flask_cors import cross_origin
from flask_cors import CORS, cross_origin

auth_bp = Blueprint('auth', __name__)
CORS(auth_bp)

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin()
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        identity={
            'user_id': user.id,
            'username': user.username, 
            'role': user.role
        }
        access_token = create_access_token(identity)
        return jsonify(access_token=access_token, user=identity), 200
    return jsonify(message="Invalid credentials"), 401
