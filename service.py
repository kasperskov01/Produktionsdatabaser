from models import UserModel

class UserService:
    def __init__(self):
        self.model = UserModel()
    
    def create(self, params):
        return self.model.create(params)