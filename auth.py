from database import Database

class Auth:
    def __init__(self):
        self.db = Database()

    def register(self, nom, prenom, email, password):
        self.db.add_user(nom, prenom, email, password)

    def login(self, email, password):
        user = self.db.get_user(email)
        if user and self.db.check_password(user['password'], password):
            return user
        return None
