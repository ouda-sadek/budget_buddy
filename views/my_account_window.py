import customtkinter as ctk
from tkinter import ttk

class MyAccountWindow(ctk.CTk):
    def __init__(self, db, email):
        super().__init__()

        self.db = db
        self.email = email
        self.title("My Account")
        self.geometry("600x500")
        self.resizable(False, False)

        # Form Title
        self.title_label = ctk.CTkLabel(self, text="My Account", font=("Arial", 24))
        self.title_label.grid(row=0, column=1, pady=10)

        # Get user details
        self.user_data = self.db.get_user_by_email(self.email)
        if not self.user_data:
            # Si l'utilisateur n'est pas trouvé
            self.error_label = ctk.CTkLabel(self, text="User not found.", font=("Arial", 16), fg="red")
            self.error_label.grid(row=1, column=0, columnspan=2, pady=20)
            return
        """user_data = self.db.get_user_by_email("user@example.com")
        self.name_label = ctk.CTkLabel(self, text=f"Name: {user_data['name']}")
        self.name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")"""
        
        self.balance = self.db.get_user_balance(self.email)

        # Créer les widgets pour afficher les données
        self.create_widgets()


        """# User Information
        user_data = self.db.get_user_by_email("user@example.com")
        self.name_label = ctk.CTkLabel(self, text=f"Name: {user_data['name']}")
        self.name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")"""

    def create_widgets(self):    
        
        # Form Title
        self.title_label = ctk.CTkLabel(self, text="My Account", font=("Arial", 24))
        self.title_label.grid(row=0, column=1, pady=20)
        
        # Display user info (Name and Email)
        self.name_label = ctk.CTkLabel(self, text=f"Name: {self.user_data['first_name']} {self.user_data['last_name']}")
        self.name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        
        self.email_label = ctk.CTkLabel(self, text=f"Email: {self.user_data['email']}")
        self.email_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        # Display account balance
        self.balance_label = ctk.CTkLabel(self, text=f"Account Balance: ${self.balance}", font=("Arial", 18))
        self.balance_label.grid(row=3, column=1, pady=20)

        # Transactions title
        self.transactions_label = ctk.CTkLabel(self, text="Recent Transactions", font=("Arial", 18))
        self.transactions_label.grid(row=4, column=0, padx=20, pady=20, sticky="w")

        # Create the transactions table
        self.create_transaction_table()

    def create_transaction_table(self):
        # Assuming you have a method to fetch transactions from the DB
        transactions = self.db.get_user_transactions(self.email)  # Cette méthode devrait renvoyer les transactions de l'utilisateur

        # Creating the table with headers
        self.transaction_table = ttk.Treeview(self, columns=("Date", "Amount", "Description"), show="headings")
        self.transaction_table.grid(row=5, column=0, columnspan=2, padx=20, pady=20)
        
        self.transaction_table.heading("Date", text="Date")
        self.transaction_table.heading("Amount", text="Amount")
        self.transaction_table.heading("Description", text="Description")

        # Insert the transaction data
        for transaction in transactions:
            self.transaction_table.insert("", "end", values=(transaction["date"], f"${transaction['amount']}", transaction["description"]))

        # Adding a scrollbar
        scrollbar = ctk.CTkScrollbar(self, command=self.transaction_table.yview)
        self.transaction_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=5, column=2, sticky="ns", padx=10, pady=20)