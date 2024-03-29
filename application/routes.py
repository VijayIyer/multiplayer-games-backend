from flask import Flask, json, request, current_app as app, session
# from flask_login import current_user, login_required
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from flask_ngrok import run_with_ngrok
from application import socket
from application.auth import auth
from application.auth import token_required, socket_token_required
from application.games.game import Game
from application.games.enums import GameState, GameType, UserType
from application.games.tic_tac_toe import TicTacToeGame
from application.games.connect4 import Connect4

@socket.on('createTicTacToeGame')
@socket_token_required
def create_new_tictactoe_game(current_user, user_info):
    print('creating new game....')
    new_game = TicTacToeGame()
    new_game.add_user(current_user)
    new_game.assign_user_turn(current_user)
    emit('newGameCreated', new_game.get_details(), broadcast=True)
    emit('newGameDetails', new_game.get_game_data(), to=request.sid)

@socket.on('getExistingTicTacToeGame')
@socket_token_required
def get_ongoing_game(current_user, game_info):
    existing_game = list(filter(lambda game: game.id == int(game_info['id']), Game._games))[0]
    emit('ongoingGameDetails', existing_game.get_game_data() , to=request.sid)

@socket.on('createConnect4Game')
@socket_token_required
def create_new_connect4_game(current_user, user_info):
    print('creating new game')
    new_game = Connect4()
    new_game.add_user(current_user)
    new_game.assign_user_turn(current_user)
    emit('newGameCreated', new_game.get_details(), broadcast=True)
    emit('newGameDetails', new_game.get_game_data(), to=request.sid)

@socket.on('getExistingConnect4Game')
@socket_token_required
def get_ongoing_connect4_game(current_user, game_info):
    existing_game = list(filter(lambda game: game.id == int(game_info['id']), Game._games))[0]
    emit('ongoingGameDetails', existing_game.get_game_data(), to=request.sid)

@socket.on('joinGame')
@socket_token_required
def join_game(current_user, game_info):
    print(f'request coming from id - {request.sid}')
    game = list(filter(lambda game: game.id == int(game_info['id']), Game._games))[0]
    print(game.get_details())
    if not game.check_user(current_user):
        game.add_user(current_user)
        game.assign_user_turn(current_user)
    print(f'joined game - {[user.id for user in game.users]}')
    print(f'sending request to id - {request.sid}')
    return game.get_details()

@socket.on('chat')
def chat(data):
    # print(f'recieved chat message:{data["msg"]}')
    socket.emit('chat', {'msg':data['msg']}, broadcast=True)

# @socket.on('join')
# def join_game():
#     user_id = request.sid
#     # print(user_id)
#     emit('joined',{'user_id':user_id})

@socket.on('connect')
def test_connect():
    #global squares
    print(f'connection request recieved from {request.sid}');
    send('connected!')

@socket.on('getAllOngoingGames')
def get_all_ongoing_games():
    # print(f'getting all onging games: {Connect4._games}')
    return list(map(lambda x: x.get_details(), Game._games))

@socket.on('move')
@socket_token_required
def move(current_user, move):
    game = Game._games[move['gameId']]
    if game.is_game_over():
        # print('game over!')
        emit('gameOver', {'id':game.id, 'winningSquares':game.winner}, to=request.sid)
        return {'squares':game.squares, 'turn':game.turn.value}
    pos = move['pos']
    game.move(current_user, pos)
    if game.winner is not None:
        emit('gameOver', {'id':game.id, 'winningSquares':game.winner, 'turn': game.turn.value}, broadcast=True)

    emit('opponentMadeMove', {'id':game.id, 'squares':game.squares, 'turn':game.turn.value}, skip_sid=request.sid, broadcast=True)
    return {'squares':game.squares, 'turn':game.turn.value}

@socket.on('connect4Move')
@socket_token_required
def make_connect4_move(current_user, move):
    
    game = Game._games[move['gameId']]
    # print(f'turn is {game.turn}')
    # game changes based on move
    pos = move['cellNumber']
    user_type = [x.user_type for x in game.users if x.id == current_user.id][0]
    user_turn = [x.turn for x in game.users if x.id == current_user.id][0]
    if(game.check_user(current_user) and game.turn == user_turn and user_type == UserType.PLAYER and int(pos) in game.allowed and game.filled[int(pos)] == -1):
        game.move(current_user, pos)
        if game.is_game_over():
            emit('connect4gameover', 
                {'winningCircles': game.winningCircles,
                'filled': game.filled,
                'allowed': game.allowed,
                'turn': game.turn.value,
                'id':game.id
                    }, broadcast=True)
        else:
            emit('connect4MoveSuccess', {
                'filled':game.filled,
                'allowed':game.allowed,
                'turn':game.turn.value,
                'winningCircles':game.winningCircles,
                'id':game.id
                }, broadcast = True)
    else:
        # print('emitting move not allowed message')
        emit('moveNotAllowed', to=request.sid)


if __name__ == "__main__":
    socket.run(app)
