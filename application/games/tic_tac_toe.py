from enum import Enum
from .user import User
from .enums import GameState, GameType, UserType
from .game import Game

class Turn(Enum):
    X=0
    O=1

class TicTacToeGame(Game):
    _games  = []
    def __init__(self, game_type = GameType.MULTIPLAYER):
        super().__init__()
        self.id = len(Game._games)
        Game._games.append(self)
        self.type = 'TicTacToe'
        self.squares = [-1 for _ in range(9)]
        self.state = GameState.NOT_STARTED
        self.game_type = game_type
        self.num_allowed_users = 2
        self.turn = Turn.X
        self.winner = None
    
    def move(self, user, pos):
        user_type = [x.user_type for x in self.users if x.id == user.id][0]
        user_turn = [x.turn for x in self.users if x.id == user.id][0]
        if self.check_user(user) and user_type == UserType.PLAYER and user_turn == self.turn and self.squares[pos] == -1:
            if self.state == GameState.NOT_STARTED:
                self.state = GameState.STARTED
            self.squares[pos] = 'X' if self.turn == Turn.X else 'O'
            
            self.winner = self.calculate_winner(self.squares)
            if self.winner is not None:
                self.state = GameState.OVER
            else:
                # update turn only if game is not over to give the other player permission to make move
                self.update_turn()
    
    # needs to be in the game interface
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
            if ((squares[a] == squares[b] == squares[c]) and (squares[a] == 'X' or squares[a] == 'O')):
                return (a,b,c)
        return None
    
    def get_game_data(self):
        return { 'id':self.id,
                'type':self.type,
                'turn':self.turn.value, 
                'squares':self.squares, 
                'winner':self.winner 
                }
