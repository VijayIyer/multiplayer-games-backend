from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins='*')


@socket.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    
@socket.on('ping')
def move(msg):
    print('recieved ping!');
    emit('pong', msg+' was recieved on server')

if __name__ == "__main__":
    socket.run(app)
