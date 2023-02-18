from enum import Enum

class GameState(Enum):
    NOT_STARTED=1
    STARTED=2
    OVER=3

class GameType(Enum):
    SINGLE_PLAYER=1
    MULTIPLAYER=2

class UserType(Enum):
    OBSERVER=1
    PLAYER=2

class Turn(Enum):
    X=0
    O=1

class User():
    def __init__(self, user_id, user_name, user_type = UserType.PLAYER):
        self.user_type = user_type
        self.id = user_id
        self.name = user_name

class TicTacToeGame:
    _games  = []
    def __init__(self, game_type = GameType.MULTIPLAYER):
        self.id = len(TicTacToeGame._games)
        TicTacToeGame._games.append(self)
        self.squares = [-1 for _ in range(9)]
        self.state = GameState.NOT_STARTED
        self.game_type = game_type
        self.users = []
        self.turn = Turn.X
        self.winner = None
    
    def __repr__(self):
        return f'game id : {self.id}, game state:{self.state}'
    def add_user(self, user):
        new_user = User(user['id'], user['name'])
        if len([user for user in self.users if user.user_type == UserType.PLAYER]) == 2:
            new_user.user_type = UserType.OBSERVER
        else:
            new_user.user_type = UserType.PLAYER
        self.users.append(user)
    
    def check_user(self, user):
        if user in self.users:
            return True
        return False
    
    def move(self, pos):
        if self.squares[pos] == -1:
            if self.state == GameState.NOT_STARTED:
                self.state = GameState.STARTED
            self.squares[pos] = 'X' if self.turn == Turn.X else 'O'
            self.update_turn()
            self.winner = self.calculate_winner(self.squares)
            if self.winner is not None:
                self.state = GameState.OVER
    
    def update_turn(self):
        if self.turn == Turn.X:
            self.turn = Turn.O
        else:
            self.turn = Turn.X

    def is_game_over(self):
        return self.state == GameState.OVER

    def calculate_winner(self, squares):
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
    
    
