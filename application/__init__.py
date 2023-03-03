# this file is so the application can be treated as a module

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

def init_app():
	app = Flask(__name__)
  CORS(app)
  socket = SocketIO(app, cors_allowed_origins='*')
	with app.app_context():
		from . import routes

	return app