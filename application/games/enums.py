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

