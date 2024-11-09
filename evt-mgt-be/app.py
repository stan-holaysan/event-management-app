from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt
from auth import auth_bp
from events import events_bp
from reservations import reservations_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True, methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type", "Authorization"])
# CORS(app, resources={r"/*": {"origins": "*"}}, methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"])

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(events_bp, url_prefix='/events')
app.register_blueprint(reservations_bp, url_prefix='/reservations')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
