# banker.py

import customtkinter as ctk
from tkinter import messagebox
from db.database import Database

class BankerLoginWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Connexion Banquier")
        self.geometry("400x300")
        self.db = Database("localhost", "root", "root", "budget_buddy")

        ctk.CTkLabel(self, text="Connexion Banquier", font=("Arial", 20)).pack(pady=20)

        ctk.CTkLabel(self, text="Email :").pack()
        self.email_entry = ctk.CTkEntry(self, placeholder_text="ex: admin@bank.fr")
        self.email_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Mot de passe :").pack()
        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Mot de passe")
        self.password_entry.pack(pady=5)

        ctk.CTkButton(self, text="Se connecter", command=self.login).pack(pady=20)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        result = self.db.execute_query("SELECT id, name, password FROM bankers WHERE email = %s", (email,))
        if not result:
            messagebox.showerror("Erreur", "Banquier non trouvé.")
            return

        banker_id, name, stored_password = result[0]

        if password == stored_password:  # 🔐 à sécuriser avec hash plus tard
            messagebox.showinfo("Bienvenue", f"Bonjour {name} !")
            # 👉 Ici tu peux appeler la future fenêtre : BankerDashboard(self, banker_id)
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
