from .user import User
from .enums import UserType

class Game:
    _games = []
    def __init__(self):
        self.users = []
        self.num_allowed_users = 2 # can be overwritten

    def check_user(self, user):
        print([user.id for user in self.users], user.id)
        if user.id in [user.id for user in self.users]:
            return True
        print(f'user does not exist')
        return False

    def add_user(self, user):
        new_user = User(user.id, user.name)
        if len([user for user in self.users if user.user_type == UserType.PLAYER]) >= self.num_allowed_users:
            new_user.user_type = UserType.OBSERVER
        else:
            new_user.user_type = UserType.PLAYER
        self.users.append(new_user)
    
    def __repr__(self):
        return f'game id : {self.id}, game state:{self.state}'
