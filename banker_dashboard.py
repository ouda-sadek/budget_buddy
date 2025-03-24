# banker_dashboard.py

import customtkinter as ctk
from account import AccountWindow
from db.database import Database

class BankerDashboard(ctk.CTkToplevel):
    def __init__(self, parent, banker_id):
        super().__init__(parent)
        self.title("Portefeuille du banquier")
        self.geometry("700x500")
        self.resizable(False, False)
        self.banker_id = banker_id
        self.db = Database("localhost", "root", "root", "budget_buddy")

        ctk.CTkLabel(self, text="Liste des clients", font=("Arial", 20, "bold")).pack(pady=20)

        self.client_listbox = ctk.CTkScrollableFrame(self, width=600, height=350)
        self.client_listbox.pack(pady=10)

        self.load_clients()

    def load_clients(self):
        query = "SELECT id, first_name, last_name, email FROM users WHERE banker_id = %s"
        clients = self.db.execute_query(query, (self.banker_id,))

        if not clients:
            ctk.CTkLabel(self.client_listbox, text="Aucun client associé.").pack()
            return

        for client in clients:
            client_id, first_name, last_name, email = client
            display_text = f"{first_name} {last_name} - {email}"
            btn = ctk.CTkButton(
                self.client_listbox,
                text=display_text,
                width=580,
                command=lambda c=client: self.open_client_account(c)
            )
            btn.pack(pady=5)

    def open_client_account(self, client):
        client_data = {
            "id": client[0],
            "first_name": client[1],
            "last_name": client[2],
            "email": client[3]
        }
        # Lance AccountWindow comme si le client était connecté
        AccountWindow(self, client_data)
    