import bcrypt
from db.database import Database  # Connexion à la base de données

class UserManager:
    def __init__(self):
        self.db = Database(host="localhost", user="root", password="root", database="budget_buddy")

    def register_user(self, first_name, last_name, email, password):
        """Inscription d’un utilisateur avec hachage du mot de passe."""
        if not self.validate_password(password):
            return False, "Mot de passe non sécurisé !"

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        try:
            self.db.execute_query(query, (first_name, last_name, email, hashed_password))
            return True, "Inscription réussie !"
        except Exception as e:
            return False, str(e)

    def login_user(self, email, password):
        """Vérification des identifiants de connexion."""
        query = "SELECT first_name, last_name, password FROM users WHERE email = %s"
        result = self.db.execute_query(query, (email,))

        if not result:
            return False, "Utilisateur non trouvé."

        user_data = result[0]
        stored_password = user_data[2]

        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            return True, {"first_name": user_data[0], "last_name": user_data[1]}
        else:
            return False, "Mot de passe incorrect."

    def validate_password(self, password):
        """Vérifie la complexité du mot de passe."""
        import re
        return (len(password) >= 10 and
                re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'\d', password) and
                re.search(r'\W', password))

