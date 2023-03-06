from .enums import UserType

class User():
    def __init__(self, user_id, user_name, user_type = UserType.PLAYER):
        self.user_type = user_type
        self.id = user_id
        self.name = user_name
