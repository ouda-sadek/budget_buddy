import mysql.connector
from mysql.connector import Error

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

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
