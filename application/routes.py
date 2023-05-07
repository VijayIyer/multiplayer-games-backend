from flask import Flask, json, request, current_app as app, session
# from flask_login import current_user, login_required
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from flask_ngrok import run_with_ngrok
from application import socket
from application.auth import auth
from application.auth import token_required, socket_token_required
from application.games.game import Game
from application.games.tic_tac_toe import GameState, GameType, UserType ,TicTacToeGame, User
from application.games.connect4 import Connect4, Turn as Connect4Turn, GameState as Connect4GameState



@app.route('/login_required')
@token_required
def login_required_route(user):
    return f'Hello login required! - {user.email}, {user.name}'

@app.route('/test')
def test():
    print([f'{k}:{v}' for k,v in request.cookies.items()])
    print('hello world!')
    return 'Hello test!'

@app.route('/test1')
@token_required
def test1(user):
    # print([f'{k}:{v}' for k,v in request.cookies.items()])
    # print('hello world!')
    return f'Hello login required test1 route! - {user.email}, {user.name}'

@app.route('/test2')
def test2():
    print([f'{k}:{v}' for k,v in request.cookies.items()])
    print('hello world!')
    return 'Hello test2!'

@socket.on('createTicTacToeGame')
@socket_token_required
def create_new_game(user_info):
    print('creating new game')
    print(f"{user_info['token']}")
    new_game = TicTacToeGame()
    new_game.add_user({'id':request.sid, 'name':user_info['name']})
    emit('newGameCreated', {'gameId': new_game.id, 'type':'Tic Tac Toe'}, broadcast=True)
    emit('newGameDetails', 
        { 
        'id':new_game.id,
        'turn':new_game.turn.value, 
        'squares':new_game.squares, 
        'winner':new_game.winner 
        } , to=request.sid)

@socket.on('getExistingTicTacToeGame')
def get_ongoing_game(game_info):
    # print(f'\ntrying to fetch game {game_info["id"]}')
    # print([game for game in TicTacToeGame._games])
    existing_game = list(filter(lambda game: game.id == int(game_info['id']), Game._games))[0]
    emit('ongoingGameDetails', 
        { 
        'id':existing_game.id, 
        'squares':existing_game.squares, 
        'turn':existing_game.turn.value, 
        'winner':existing_game.winner
        } , to=request.sid)

@socket.on('createConnect4Game')
def create_new_connect4_game(user_info):
    print('creating new game')
    new_game = Connect4()
    new_game.add_user({'id':request.sid, 'name':user_info['name']})
    emit('newGameCreated', {'gameId': new_game.id, 'type':'Connect4'}, broadcast=True)
    emit('newConnect4GameDetails', { 'id':new_game.id, 'allowed':new_game.allowed, 'filled':new_game.filled, 'winningCircles':new_game.winningCircles } , to=request.sid)

@socket.on('getExistingConnect4Game')
def get_ongoing_connect4_game(game_info):
    #print(f'\ntrying to fetch game {game_info["id"]}')
    #print([game for game in Connect4._games])
    existing_game = list(filter(lambda game: game.id == int(game_info['id']), Game._games))[0]
    emit('ongoingConnect4GameDetails', 
        { 'id':existing_game.id,
         'filled':existing_game.filled, 
         'allowed':existing_game.allowed, 
         'winningCircles':existing_game.winningCircles if existing_game.winningCircles is not None else None,
         'turn':existing_game.turn.value } , to=request.sid)

@socket.on('chat')
def chat(data):
    # print(f'recieved chat message:{data["msg"]}')
    socket.emit('chat', {'msg':data['msg']}, broadcast=True)

@socket.on('join')
def join_game():
    user_id = request.sid
    # print(user_id)
    emit('joined',{'user_id':user_id})

@socket.on('connect')
def test_connect():
    #global squares
    print(f'connection request recieved from {request.sid}');
    send('connected!')

@socket.on('getAllOngoingGames')
def get_all_ongoing_games():
    # print(f'getting all onging games: {Connect4._games}')
    return list(map(lambda x: {'gameId':x.id, 'type':x.type}, Game._games))

@socket.on('move')
def move(move):
    print(Game._games)
    game = Game._games[move['gameId']]
    if game.is_game_over():
        # print('game over!')
        emit('gameOver', {'id':game.id, 'winningSquares':game.winner}, to=request.sid)
        return {'squares':game.squares, 'turn':game.turn.value}
    pos = move['pos']
    game.move(pos)
    if game.winner is not None:
        emit('gameOver', {'id':game.id, 'winningSquares':game.winner, 'turn': game.turn.value}, broadcast=True)

    emit('opponentMadeMove', {'id':game.id, 'squares':game.squares, 'turn':game.turn.value}, skip_sid=request.sid, broadcast=True)
    return {'squares':game.squares, 'turn':game.turn.value}

@socket.on('connect4Move')
def make_connect4_move(move):
    
    game = Game._games[move['gameId']]
    # print(f'turn is {game.turn}')
    # game changes based on move
    pos = move['cellNumber']
    if(int(pos) in game.allowed and game.filled[int(pos)] == -1):
        game.move(pos)
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
