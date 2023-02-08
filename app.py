from flask import Flask, json
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins='*')
squares = [-1 for i in range(9)]
turn = 0
gameOver=False

def calculate_winner(squares):
    if((squares[0] == squares[4] == squares[8] == 'X') or (squares[0] == squares[4] == squares[8] == 'O')):
        return True
    if((squares[1] == squares[4] == squares[7] == 'X') or (squares[1] == squares[4] == squares[7] == 'O')):
        return True
    if((squares[2] == squares[4] == squares[6] == 'X') or (squares[2] == squares[4] == squares[6] == 'O')):
        return True
    if((squares[3] == squares[4] == squares[5] == 'X') or (squares[3] == squares[4] == squares[5] == 'O')):
        return True
    if((squares[0] == squares[1] == squares[2] == 'X') or (squares[0] == squares[1] == squares[2] == 'O')):
        return True
    if((squares[0] == squares[3] == squares[6] == 'X') or (squares[0] == squares[3] == squares[6] == 'O')):
        return True
    if((squares[6] == squares[7] == squares[8] == 'X') or (squares[6] == squares[7] == squares[8] == 'O')):
        return True
    if((squares[2] == squares[5] == squares[8] == 'X') or (squares[2] == squares[5] == squares[8] == 'O')):
        return True
    return False

@socket.on('connect')
def test_connect():
    global squares
    print(f'sending initial data {squares}');
    emit('sending initial data', {'squares': squares})
    
@socket.on('ping')
def move(msg):
    print('recieved ping!');
    emit('pong', msg+' was recieved on server')

@socket.on('move')
def move(move):
    global gameOver
    global squares
    global turn
    print(squares)
    if gameOver:
        emit('gameOver', {'squares':squares, 'gameOver':True}, broadcast=True)
    else:
        
        pos = move['pos']
        print(f'{pos} clicked')
        if squares[pos] == -1:
            squares[pos] = 'X' if turn == 0 else 'O'
            if calculate_winner(squares):
                emit('gameOver', {'squares':squares, 'gameOver':True}, broadcast=True)
                gameOver=True
            else:
                emit('recieved', {'squares':squares, 'turn':1 if turn == 0 else 0}, broadcast=True)
        else:
            print('emitting error')
            emit('error', {'message':'square already used'})
        if turn == 1:
            turn = 0
        else: turn = 1

if __name__ == "__main__":
    socket.run(app)
