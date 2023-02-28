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
    BLUE=0
    RED=1

class User():
    def __init__(self, user_id, user_name, user_type = UserType.PLAYER):
        self.user_type = user_type
        self.id = user_id
        self.name = user_name

class Connect4:
    _games  = []
    def __init__(self, game_type = GameType.MULTIPLAYER, num_rows = 8, num_cols = 6):
        self.id = len(Connect4._games)
        Connect4._games.append(self)
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.filled = [-1 for _ in range(num_rows * num_cols)]
        self.allowed = [i for i in range((num_rows - 1) * num_cols, (num_rows* num_cols))]
        self.winningCircles = []
        self.state = GameState.NOT_STARTED
        self.game_type = game_type # for later, AI agent
        self.users = []
        self.turn = Turn.RED
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
        if self.state == GameState.NOT_STARTED:
            self.state = GameState.STARTED
        pos = int(pos)
        self.filled[pos] = 'red' if self.turn == Turn.RED else 'blue'
        self.allowed.append(pos - 6)
        self.update_turn()
    
    def update_turn(self):
        if self.turn == Turn.BLUE:
            self.turn = Turn.RED
        else:
            self.turn = Turn.BLUE

    def is_game_over(self):
        return self.state == GameState.OVER or (self.checkVerticalCells() or self.checkHorizontalCells() or self.checkLeftRightCells() or self.checkRightLeftCells())

    def checkVerticalCells():
        return false

    def checkHorizontalCells():
        return false

    def checkLeftRightCells():
        return false

    def checkRightLeftCells():
        return false

    def calculate_winner(self, squares):
        return None
    
    
