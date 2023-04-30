from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

socket = SocketIO()
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    socket.init_app(app,  cors_allowed_origins='*')
    CORS(app)
    db.init_app(app)
    with app.app_context():
        from . import auth
        from . import routes
        from . import models
        # Create Database Models
        db.create_all()
    return app
