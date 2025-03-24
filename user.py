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
            # ➕ Insertion de l'utilisateur
            self.db.execute_query(query, (first_name, last_name, email, hashed_password))

            # ✅ Récupération de l'id de l'utilisateur
            result = self.db.execute_query("SELECT id FROM users WHERE email = %s", (email,))
            if result:
                user_id = result[0][0]
                # ➕ Création du compte associé
                self.db.execute_query("INSERT INTO accounts (user_id, balance) VALUES (%s, 0.00)", (user_id,))

            return True, "Inscription réussie !"

        except Exception as e:
            return False, str(e)

    def login_user(self, email, password):
        """Vérification des identifiants de connexion."""
        query = "SELECT id, first_name, last_name, password FROM users WHERE email = %s"
        result = self.db.execute_query(query, (email,))

        if not result:
            return False, "Utilisateur non trouvé."

        user_data = result[0]
        user_id = user_data[0]
        first_name = user_data[1]
        last_name = user_data[2]
        stored_password = user_data[3]

        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            return True, {
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name
            }
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
