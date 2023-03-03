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
    RED=0
    BLUE=1

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
        self.verticalCellsInARow = None
        self.horizontalCellsInARow = None
        self.leftRightCellsInARow = None
        self.rightLeftCellsInARow = None
    
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
        if self.is_game_over():
            self.winningCircles = self.calculate_winner()
            print(f'winnign circles - {self.winner}')
        else:
            self.update_turn()
    
    def update_turn(self):
        if self.turn == Turn.BLUE:
            self.turn = Turn.RED
        else:
            self.turn = Turn.BLUE

    def is_game_over(self):
        if self.state == GameState.OVER:
            return True
        self.verticalCellsInARow = self.checkVerticalCells()
        self.horizontalCellsInARow = self.checkHorizontalCells()
        self.leftRightCellsInARow = self.checkLeftRightCells()
        self.rightLeftCellsInARow = self.checkRightLeftCells()
        print(f'vertical cell indexes {self.verticalCellsInARow}')
        if (self.verticalCellsInARow is not None \
            or self.horizontalCellsInARow is not None \
            or self.leftRightCellsInARow is not None \
            or self.rightLeftCellsInARow is not None):
            print('line 82 game over!!')
            self.state = GameState.OVER
            return True 
        return False

    def checkVerticalCells(self):
        result  = False
        rows = self.num_rows;
        cols = self.num_cols;
        for i in range(rows - 3):
            for j in range(cols):
                print(i, j)
                values = [self.filled[i*cols+j], self.filled[(i+1)*cols+j], self.filled[(i+2)*cols+j], self.filled[(i+3)*cols+j]]
                if all(x == values[0] for x in values) and (self.filled[i * cols + j] == 'blue' or self.filled[i * cols + j] == 'red'):
                    print([(i*cols)+j, (i+1)*cols + j, (i+2)*cols+j, (i+3)*cols+j])
                    return [(i*cols)+j, (i+1)*cols + j, (i+2)*cols+j, (i+3)*cols+j]
        return None

    def checkHorizontalCells(self):
        result  = False
        rows = self.num_rows;
        cols = self.num_cols;
        for i in range(rows):
            for j in range(cols - 3):
                print(i, j)
                values = [self.filled[i*cols+j], self.filled[i*cols+(j+1)], self.filled[i*cols+(j+2)], self.filled[i*cols+(j+3)]]
                if all(x == values[0] for x in values) and (self.filled[i * cols + j] == 'blue' or self.filled[i * cols + j] == 'red'):
                    print([i*cols+j, i*cols + (j+1), i*cols+(j+2), i*cols+(j+3)])
                    return [i*cols+j, i*cols + (j+1), i*cols+(j+2), i*cols+(j+3)]
        return None

    def checkLeftRightCells(self):
        result  = False
        rows = self.num_rows;
        cols = self.num_cols;
        for i in range(rows - 3):
            for j in range(cols - 1, cols - 3, -1):
                print(i, j)
                values = [self.filled[i*cols+j], self.filled[(i+1)*cols+(j - 1)], self.filled[(i+2)*cols+(j - 2)], self.filled[(i+3)*cols+(j - 3)]]
                if all(x == values[0] for x in values) and (self.filled[i * cols + j] == 'blue' or self.filled[i * cols + j] == 'red'):
                    print([(i*cols)+j, (i+1)*cols + (j - 1), (i+2)*cols+(j - 2), (i+3)*cols+(j - 3)])
                    return [(i*cols)+j, (i+1)*cols + (j - 1), (i+2)*cols+(j - 1), (i+3)*cols+(j - 3)]
        return None

    def checkRightLeftCells(self):
        result  = False
        rows = self.num_rows;
        cols = self.num_cols;
        for i in range(rows - 3):
            for j in range(cols - 3):
                print(i, j)
                values = [self.filled[i*cols+j], self.filled[(i+1)*cols+(j+1)], self.filled[(i+2)*cols+(j+2)], self.filled[(i+3)*cols+(j+3)]]
                if all(x == values[0] for x in values) and (self.filled[i * cols + j] == 'blue' or self.filled[i * cols + j] == 'red'):
                    print([(i*cols)+j, (i+1)*cols + (j+1), (i+2)*cols+(j+2), (i+3)*cols+(j+3)])
                    return [(i*cols)+j, (i+1)*cols + (j+1), (i+2)*cols+(j+2), (i+3)*cols+(j+3)]
        return None

    def calculate_winner(self):
        if self.verticalCellsInARow is not None:
            return self.verticalCellsInARow
        if self.horizontalCellsInARow is not None:
            return self.horizontalCellsInARow
        if self.leftRightCellsInARow is not None:
            return self.leftRightCellsInARow
        if self.rightLeftCellsInARow is not None:
            return self.rightLeftCellsInARow
    
    
