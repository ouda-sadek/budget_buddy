import customtkinter as ctk
from auth import Auth
from transaction import TransactionManager

class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.auth = Auth()
        self.transaction_manager = None
        self.title("Gestion Financière")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Email")
        self.email_entry.pack(pady=10, padx=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=10, padx=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Connexion", command=self.login)
        self.login_button.pack(pady=10, padx=10)

        self.register_button = ctk.CTkButton(self.login_frame, text="Inscription", command=self.show_register_frame)
        self.register_button.pack(pady=10, padx=10)

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.nom_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Nom")
        self.nom_entry.pack(pady=10, padx=10)

        self.prenom_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Prénom")
        self.prenom_entry.pack(pady=10, padx=10)

        self.email_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Email")
        self.email_entry.pack(pady=10, padx=10)

        self.password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=10, padx=10)

        self.register_button = ctk.CTkButton(self.register_frame, text="S'inscrire", command=self.register)
        self.register_button.pack(pady=10, padx=10)

        self.back_button = ctk.CTkButton(self.register_frame, text="Retour", command=self.show_login_frame)
        self.back_button.pack(pady=10, padx=10)

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(pady=20, padx=20, fill='both', expand=True)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = self.auth.login(email, password)
        if user:
            self.transaction_manager = TransactionManager(user['id'])
            self.show_main_frame()
        else:
            ctk.CTkMessageBox.show_error("Erreur", "Email ou mot de passe incorrect")

    def register(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.auth.register(nom, prenom, email, password)
        self.show_login_frame()

    def show_main_frame(self):
        self.login_frame.pack_forget()
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.transactions_list = ctk.CTkTextbox(self.main_frame)
        self.transactions_list.pack(pady=10, padx=10, fill='both', expand=True)

        self.refresh_transactions()

        self.add_transaction_button = ctk.CTkButton(self.main_frame, text="Ajouter une transaction", command=self.show_add_transaction_frame)
        self.add_transaction_button.pack(pady=10, padx=10)

    def refresh_transactions(self):
        self.transactions_list.delete(1.0, ctk.END)
        transactions = self.transaction_manager.get_transactions()
        for transaction in transactions:
            self.transactions_list.insert(ctk.END, f"{transaction['reference']} - {transaction['description']} - {transaction['montant']} - {transaction['date']} - {transaction['type']}\n")

    def show_add_transaction_frame(self):
        self.add_transaction_frame = ctk.CTkFrame(self.main_frame)
        self.add_transaction_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.reference_entry = ctk.CTkEntry(self.add_transaction_frame, placeholder_text="Référence")
        self.reference_entry.pack(pady=10, padx=10)

        self.description_entry = ctk.CTkEntry(self.add_transaction_frame, placeholder_text="Description")
        self.description_entry.pack(pady=10, padx=10)

        self.montant_entry = ctk.CTkEntry(self.add_transaction_frame, placeholder_text="Montant")
        self.montant_entry.pack(pady=10, padx=10)

        self.date_entry = ctk.CTkEntry(self.add_transaction_frame, placeholder_text="Date")
        self.date_entry.pack(pady=10, padx=10)

        self.type_entry = ctk.CTkEntry(self.add_transaction_frame, placeholder_text="Type")
        self.type_entry.pack(pady=10, padx=10)

        self.add_button = ctk.CTkButton(self.add_transaction_frame, text="Ajouter", command=self.add_transaction)
        self.add_button.pack(pady=10, padx=10)

        self.back_button = ctk.CTkButton(self.add_transaction_frame, text="Retour", command=self.hide_add_transaction_frame)
        self.back_button.pack(pady=10, padx=10)

    def hide_add_transaction_frame(self):
        self.add_transaction_frame.pack_forget()

    def add_transaction(self):
        reference = self.reference_entry.get()
        description = self.description_entry.get()
        montant = self.montant_entry.get()
        date = self.date_entry.get()
        type = self.type_entry.get()
        self.transaction_manager.add_transaction(reference, description, montant, date, type)
        self.refresh_transactions()
        self.hide_add_transaction_frame()

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
