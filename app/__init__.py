from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socket = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    socket.init_app(app,  cors_allowed_origins='*')
    CORS(app)
    with app.app_context():
        from . import routes
    
    return app
