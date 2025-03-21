import mysql.connector
from mysql.connector import Error


def create_database():
    # Connect to MySQL to create the database
    conn = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password=""
    )  
    if conn.is_connected():
            print("Successful connection to MySQL server")
    cursor = conn.cursor()
    
    # Creating the database
    cursor.execute("CREATE DATABASE IF NOT EXISTS budget_buddy")
    cursor.execute("USE budget_buddy")

    # Creating tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bankers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    banker_id INT,
    account_number VARCHAR(255) UNIQUE,
    account_type ENUM('checking', 'savings', 'credit') DEFAULT 'checking',
    balance DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (banker_id) REFERENCES bankers(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    reference VARCHAR(255) UNIQUE,
    description VARCHAR(255),
    amount DECIMAL(10, 2),
    transaction_type ENUM('deposit', 'withdrawal', 'transfer'),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banker_client_relationship (
    banker_id INT,
    client_id INT,
    PRIMARY KEY (banker_id, client_id),
    FOREIGN KEY (banker_id) REFERENCES bankers(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
    )"
    """)

    conn.commit()
    conn.close()

# Create the database and tables
create_database()
