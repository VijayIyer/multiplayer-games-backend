from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

socket = SocketIO()
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    socket.init_app(app,  cors_allowed_origins='*')
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        
        from . import auth
        from . import routes
        from . import models
        # Create Database Models
        db.create_all()
        @login_manager.user_loader
        def load_user(user_id):
            """Check if user is logged-in on every page load."""
            print('loading user')
            if user_id is not None:
                return User.query.get(user_id)
            return None
    return app
