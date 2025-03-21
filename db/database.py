import mysql.connector
from mysql.connector import Error
import bcrypt

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            self.cursor = self.connection.cursor()
            print("Successful connection to MySQL server.")
        except mysql.connector.Error as err:
            print(f"Error : {err}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # For SELECT queries, you retrieve the results
            if query.strip().lower().startswith("select"):
                # Retrieve all query results
                return self.cursor.fetchall()  
            else:
                # For INSERT, UPDATE, DELETE queries
                self.connection.commit()
                print("Query executed successfully.")  

        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return None
        
    def insert_user_data(self, first_name, last_name, email, hashed_password):
        
        query = """
            INSERT INTO clients  (first_name, last_name, email, password)
            VALUES (%s, %s, %s, %s)
        """
        params = (first_name, last_name, email, hashed_password)
            
        print(f"Executing query: {query} with params {params}")  # Débogage : affiche la requête et les paramètres
            
        result = self.execute_query(query, params)
        
        if result is not None:
            return False
        return True

    def email_exists(self, email):
        # Check if the email already exists in the database
        query = "SELECT COUNT(*) FROM clients  WHERE email = %s"
        result = self.execute_query(query, (email,))
        return result and result[0][0] > 0
    
    def get_user_by_email(self, email):
        query = "SELECT first_name, last_name, email FROM clients WHERE email = %s"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()
        
        if result:
            # Retourne un dictionnaire avec les informations de l'utilisateur
            return {"first_name": result[0], "last_name": result[1], "email": result[2]}
        
        return None  # Si aucun utilisateur n'est trouvé

    
    def get_hashed_password(self, email):
        """Retourne le mot de passe haché d'un utilisateur basé sur son email."""
        query = "SELECT password FROM clients  WHERE email = %s"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Le mot de passe haché est dans la première colonne de la ligne retournée
        return None
    
    def verify_password(self, password, hashed_password):
        """Vérifie si le mot de passe saisi correspond au mot de passe haché stocké dans la base de données."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def get_user_balance(self, email):
        """Calcule le solde de l'utilisateur en fonction de ses transactions."""
        query = """
            SELECT SUM(amount) 
            FROM transactions 
            WHERE email = %s
        """
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Retourne la somme des montants des transactions
        return 0  # Retourne 0 si l'utilisateur n'a pas de transactions


    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
