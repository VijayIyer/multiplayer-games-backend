from enum import Enum
from .user import User
from .enums import GameState, GameType, UserType
from .game import Game

class Turn(Enum):
    RED=0
    BLUE=1

class Connect4(Game):
    def __init__(self, game_type = GameType.MULTIPLAYER, num_rows = 8, num_cols = 6):
        super().__init__()
        self.id = len(Game._games)
        Game._games.append(self)
        self.type = 'Connect4'
        self.num_allowed_users = 2
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.filled = [-1 for _ in range(num_rows * num_cols)]
        self.allowed = [i for i in range((num_rows - 1) * num_cols, (num_rows* num_cols))]
        self.winningCircles = []
        self.state = GameState.NOT_STARTED
        self.game_type = game_type # for later, AI agent
        self.turn = Turn.RED
        self.winner = None
        self.verticalCellsInARow = None
        self.horizontalCellsInARow = None
        self.leftRightCellsInARow = None
        self.rightLeftCellsInARow = None
        
    
    def move(self, user, pos):
        if self.check_user(user):
            if self.state == GameState.NOT_STARTED:
                self.state = GameState.STARTED
            pos = int(pos)
            self.filled[pos] = 'red' if self.turn == Turn.RED else 'blue'
            self.allowed.append(pos - 6)
            if self.is_game_over():
                self.winningCircles = self.calculate_winner()
                # print(f'winnign circles - {self.winner}')
            else:
                self.update_turn()

    def assign_user_turn(self, user, turn):

        for i in range(len(self.users)):
            if user.id == self.users[i].id:
                self.users[i].turn = turn = Turn.RED if turn == 'Red' else Turn.BLUE

    # needs to be in game interface?
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
        # print(f'vertical cell indexes {self.verticalCellsInARow}')
        if (self.verticalCellsInARow is not None \
            or self.horizontalCellsInARow is not None \
            or self.leftRightCellsInARow is not None \
            or self.rightLeftCellsInARow is not None):
            # print('line 82 game over!!')
            self.state = GameState.OVER
            return True 
        return False

    def checkVerticalCells(self):
        result  = False
        rows = self.num_rows;
        cols = self.num_cols;
        # print('checking vertical cells')
        for i in range(rows - 3):
            for j in range(cols):
                values = [self.filled[i*cols+j], self.filled[(i+1)*cols+j], self.filled[(i+2)*cols+j], self.filled[(i+3)*cols+j]]
                if all(x == values[0] for x in values) and (self.filled[i * cols + j] == 'blue' or self.filled[i * cols + j] == 'red'):
                    # print([(i*cols)+j, (i+1)*cols + j, (i+2)*cols+j, (i+3)*cols+j])
                    return [(i*cols)+j, (i+1)*cols + j, (i+2)*cols+j, (i+3)*cols+j]
        return None

    def checkHorizontalCells(self):
        result  = False
        rows = self.num_rows;
        cols = self.num_cols;
        # print('checking horizontal cells')
        for i in range(rows):
            for j in range(cols - 3):
                values = [self.filled[i*cols+j], self.filled[i*cols+(j+1)], self.filled[i*cols+(j+2)], self.filled[i*cols+(j+3)]]
                if all(x == values[0] for x in values) and (self.filled[i * cols + j] == 'blue' or self.filled[i * cols + j] == 'red'):
                    # print([i*cols+j, i*cols + (j+1), i*cols+(j+2), i*cols+(j+3)])
                    return [i*cols+j, i*cols + (j+1), i*cols+(j+2), i*cols+(j+3)]
        return None

    def checkLeftRightCells(self):
        result  = False
        rows = self.num_rows
        cols = self.num_cols
        # print('checking leftright cells')
        for i in range(rows - 3):
            for j in range(cols - 1, cols - 4, -1):
                
                values = [self.filled[i*cols+j], self.filled[(i+1)*cols+(j - 1)], self.filled[(i+2)*cols+(j - 2)], self.filled[(i+3)*cols+(j - 3)]]
                if all(x == values[0] for x in values) and (self.filled[i * cols + j] == 'blue' or self.filled[i * cols + j] == 'red'):
                    # print([(i*cols)+j, (i+1)*cols + (j - 1), (i+2)*cols+(j - 2), (i+3)*cols+(j - 3)])
                    return [(i*cols)+j, (i+1)*cols + (j - 1), (i+2)*cols+(j - 2), (i+3)*cols+(j - 3)]
        return None

    def checkRightLeftCells(self):
        result  = False
        rows = self.num_rows
        cols = self.num_cols
        # print('checking rightleft cells')
        for i in range(rows - 3):
            for j in range(cols - 3):
                values = [self.filled[i*cols+j], self.filled[(i+1)*cols+(j+1)], self.filled[(i+2)*cols+(j+2)], self.filled[(i+3)*cols+(j+3)]]
                if all(x == values[0] for x in values) and (self.filled[i * cols + j] == 'blue' or self.filled[i * cols + j] == 'red'):
                    # print([(i*cols)+j, (i+1)*cols + (j+1), (i+2)*cols+(j+2), (i+3)*cols+(j+3)])
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
    
    def get_game_data(self):
        return { 
        'id':self.id, 
        'type':self.type,
        'allowed':self.allowed, 
        'filled':self.filled, 
        'winningCircles':self.winningCircles if self.winningCircles is not None else None,
        'turn':self.turn.value
        }
