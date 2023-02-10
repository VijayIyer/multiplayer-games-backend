from flask import Flask, json
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins='*')
squares = [-1 for _ in range(9)]
turn = 0
gameOver=False

def initialize_game():
    global squares
    global gameOver
    global turn

    squares = [-1 for _ in range(9)]
    gameOver = False
    turn = 0 
    return {'squares':squares, 'turn':turn, 'gameOver':gameOver}

def calculate_winner(squares):
    lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
    for i in range(len(lines)):
        a, b, c = lines[i]
        print(a, b, c)
        if ((squares[a] == squares[b] == squares[c]) and (squares[a] == 'X' or squares[a] == 'O')):
            return (a,b,c)
    return None

@socket.on('connect')
def test_connect():
    global squares
    print(f'sending initial data {squares}');
    emit('sending initial data', {'squares': squares})
    
@socket.on('ping')
def move(msg):
    print('recieved ping!');
    emit('pong', msg+' was recieved on server')

@socket.on('restart')
def restart():
    return initialize_game()
    

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
            winningSquares = calculate_winner(squares) 
            if winningSquares is not None:
                emit('gameOver', {'squares':squares, 'gameOver':True, 'winningSquares':winningSquares}, broadcast=True)
                gameOver=True
            else:
                emit('recieved', {'squares':squares, 'turn':1 if turn == 0 else 0}, broadcast=True)
        else:
            print('emitting error')
            emit('error', {'message':f'square {pos} already used'})
        if turn == 1:
            turn = 0
        else: turn = 1

if __name__ == "__main__":
    socket.run(app)
