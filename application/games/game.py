from .user import User
from .enums import UserType

class Game:
    _games = []
    def __init__(self):
        self.users = []

    def check_user(self, user):
        if user in self.users:
            return True
        return False

    def add_user(self, user):
        new_user = User(user['id'], user['name'])
        if len([user for user in self.users if user.user_type == UserType.PLAYER]) == 2:
            new_user.user_type = UserType.OBSERVER
        else:
            new_user.user_type = UserType.PLAYER
        self.users.append(user)
    
    def __repr__(self):
        return f'game id : {self.id}, game state:{self.state}'
