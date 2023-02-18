from flask import Flask, json, request
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from flask_ngrok import run_with_ngrok
from tic_tac_toe import GameState, GameType, UserType ,TicTacToeGame, User

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins='*')
CORS(app)
run_with_ngrok(app)

@app.route('/')
def test():
    return 'Hello World!'

@socket.on('createTicTacToeGame')
def create_new_game(user_info):
    new_game = TicTacToeGame()
    new_game.add_user({'id':request.sid, 'name':user_info['name']})
    emit('newGameCreated', {'gameId': new_game.id, 'type':'Tic Tac Toe'}, broadcast=True)
    emit('newGameDetails', { 'id':new_game.id, 'squares':new_game.squares } , to=request.sid)

@socket.on('getExistingTicTacToeGame')
def get_ongoing_game(game_info):
    print(f'\ntrying to fetch game {game_info["id"]}')
    print([game for game in TicTacToeGame._games])
    existing_game = list(filter(lambda game: game.id == int(game_info['id']), TicTacToeGame._games))[0]
    emit('ongoingGameDetails', { 'id':existing_game.id, 'squares':existing_game.squares } , to=request.sid)

@socket.on('chat')
def chat(data):
    print(f'recieved chat message:{data["msg"]}')
    socket.emit('chat', {'msg':data['msg']}, broadcast=True)

@socket.on('join')
def join_game():
    user_id = request.sid
    print(user_id)
    emit('joined',{'user_id':user_id})

@socket.on('connect')
def test_connect():
    #global squares
    print(f'connection request recieved from {request.sid}');
    send('connected!')

@socket.on('getAllOngoingGames')
def get_all_ongoing_games():
    print(f'getting all onging games: {TicTacToeGame._games}')
    return list(map(lambda x: {'gameId':x.id, 'type':'Tic Tac Toe'}, TicTacToeGame._games))

@socket.on('move')
def move(move):
    game = TicTacToeGame._games[move['gameId']]
    if game.is_game_over():
        print('game over!')
        emit('gameOver', {'winningSquares':game.winner}, to=request.sid)
        return {'squares':game.squares, 'turn':game.turn.value}
    pos = move['pos']
    game.move(pos)
    if game.winner is not None:
        emit('gameOver', {'winningSquares':game.winner}, broadcast=True)
    emit('opponentMadeMove', {'squares':game.squares, 'turn':game.turn.value}, skip_sid=request.sid, broadcast=True)
    return {'squares':game.squares, 'turn':game.turn.value}

if __name__ == "__main__":
    socket.run(app)
