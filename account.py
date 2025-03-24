import customtkinter as ctk
from db.database import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from datetime import datetime
from PIL import Image
import os



class AccountWindow(ctk.CTkToplevel):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.title("Mon Compte")
        self.geometry("1200x700")
        self.resizable(False, False)
        # 📸 Fond d'écran (juste après super().__init__())
        image_path = os.path.join(os.path.dirname(__file__), "images", "DNR.jpg")

        if os.path.exists(image_path):
            print("✅ Image trouvée :", image_path)  # Debug
            self._bg_image = Image.open(image_path)  # <- stockée dans self
            self._bg_photo = ctk.CTkImage(self._bg_image, size=(1200, 700))  # <- stockée dans self
            self._bg_label = ctk.CTkLabel(self, image=self._bg_photo, text="")
            self._bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
            
            
        else:
            print("❌ Image de fond non trouvée :", image_path)
        

        self.user_data = user_data
        # 🔧 Connexion à la base de données
        self.db = Database(
            host="localhost",
            user="root",
            password="root",
            database="budget_buddy"
        )

       

        # Layout global : menu à gauche + zone principale à droite
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="right", fill="both", expand=True)

        self._bg_label.lower()

        # Titre utilisateur
        ctk.CTkLabel(self.sidebar, text=f"{user_data['first_name']} {user_data['last_name']}", font=("Arial", 16, "bold")).pack(pady=20)

        # Boutons du menu
        ctk.CTkButton(self.sidebar, text="➕ Dépôt", command=self.show_deposit_view,width=140,height=30,corner_radius=10,fg_color="#669966",hover_color="#224466",font=("Segoe UI", 14)).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="➖ Retrait", command=self.show_withdraw_view,width=140,height=30,corner_radius=10,fg_color="#669966",hover_color="#224466",font=("Segoe UI", 14)).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="🔁 Transfert", command=self.show_transfer_view,width=140,height=30,corner_radius=10,fg_color="#669966",hover_color="#224466",font=("Segoe UI", 14)).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar,text="📜 Historique",command=self.show_history_view,width=140,height=30,corner_radius=10,fg_color="#669966",hover_color="#224466",font=("Segoe UI", 14)).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="🏠 Vue globale", command=self.show_overview,width=140,height=30,corner_radius=10,fg_color="#669966",hover_color="#224466",font=("Segoe UI", 14)).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="🚪 Quitter", command=self.quit_to_main,width=140,height=30,corner_radius=10,fg_color="#669966",hover_color="#224466",font=("Segoe UI", 14)).pack(pady=10, padx=10)

        self.show_welcome_view()

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_welcome_view(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Bienvenue dans votre espace financier !", font=("Arial", 20)).pack(pady=50)

    def show_deposit_view(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Dépôt d'argent", font=("Arial", 18)).pack(pady=20)

        # Champ Montant
        ctk.CTkLabel(self.main_area, text="Montant:").pack()
        amount_entry = ctk.CTkEntry(self.main_area, placeholder_text="Ex: 100.00")
        amount_entry.pack(pady=5)

        # Champ Description
        ctk.CTkLabel(self.main_area, text="Description:").pack()
        description_entry = ctk.CTkEntry(self.main_area, placeholder_text="Ex: Salaire, remboursement...")
        description_entry.pack(pady=5)

        # Champ Catégorie
        ctk.CTkLabel(self.main_area, text="Catégorie:").pack()
        category_entry = ctk.CTkEntry(self.main_area, placeholder_text="Ex: Travail, cadeau, autre...")
        category_entry.pack(pady=5)

        # Bouton de validation
        def submit_deposit():
            amount = amount_entry.get()
            description = description_entry.get()
            category = category_entry.get()

            try:
                amount = float(amount)
            except ValueError:
                ctk.CTkLabel(self.main_area, text="Montant invalide", text_color="red").pack()
                return

            if amount <= 0:
                ctk.CTkLabel(self.main_area, text="Montant doit être supérieur à 0", text_color="red").pack()
                return

            try:
                # 🔍 Obtenir l'ID du compte
                result = self.db.execute_query("SELECT id FROM accounts WHERE user_id = %s", (self.user_data["id"],))
                if not result:
                    ctk.CTkLabel(self.main_area, text="Compte introuvable.", text_color="red").pack()
                    return
                account_id = result[0][0]

                # 💾 Insertion de la transaction
                self.db.execute_query(
                    "INSERT INTO transactions (account_id, amount, description, category, transaction_type) VALUES (%s, %s, %s, %s, 'deposit')",
                    (account_id, amount, description, category)
                )

                # 💰 Mise à jour du solde
                self.db.execute_query(
                    "UPDATE accounts SET balance = balance + %s WHERE id = %s",
                    (amount, account_id)
                )

                ctk.CTkLabel(self.main_area, text=f"Dépôt de {amount:.2f} € enregistré avec succès ✅", text_color="green").pack(pady=10)

            except Exception as e:
                print(f"[ERREUR DÉPÔT] {e}")
                ctk.CTkLabel(self.main_area, text=f"Erreur : {e}", text_color="red").pack()

        ctk.CTkButton(self.main_area, text="Valider le dépôt", command=submit_deposit).pack(pady=20)

    
    def show_withdraw_view(self):
        self.clear_main_area()
        
        ctk.CTkLabel(self.main_area, text="Retrait d'argent", font=("Arial", 18)).pack(pady=20)

        ctk.CTkLabel(self.main_area, text="Montant :").pack()
        amount_entry = ctk.CTkEntry(self.main_area, placeholder_text="Ex: 50.00")
        amount_entry.pack(pady=5)

        ctk.CTkLabel(self.main_area, text="Description :").pack()
        description_entry = ctk.CTkEntry(self.main_area, placeholder_text="Ex: courses, sortie...")
        description_entry.pack(pady=5)

        ctk.CTkLabel(self.main_area, text="Catégorie :").pack()
        category_entry = ctk.CTkEntry(self.main_area, placeholder_text="Ex: Loisir, courses...")
        category_entry.pack(pady=5)

        def submit_withdrawal():
           try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Montant invalide")

                description = description_entry.get()
                category = category_entry.get()
                # Récupération de l'account_id
                query = "SELECT id, balance FROM accounts WHERE user_id = %s"
                result = self.db.execute_query(query, (self.user_data["id"],))
                if not result:
                    ctk.CTkLabel(self.main_area, text="Compte non trouvé.", text_color="red").pack()
                    return

                account_id, current_balance = result[0]
                print(f"[DEBUG] Solde actuel = {current_balance}")
                print(f"[DEBUG] Montant demandé = {amount}")
                if current_balance < amount:
                    ctk.CTkLabel(self.main_area, text="Solde insuffisant ❌", text_color="red").pack()
                    return
                # Enregistrer le retrait dans transactions
                insert_query = """
                INSERT INTO transactions (account_id, description, amount, category, transaction_type)
                VALUES (%s, %s, %s, %s, 'withdrawal')
                """
                self.db.execute_query(insert_query, (account_id, description, amount, category))
                # Mettre à jour le solde
                update_query = "UPDATE accounts SET balance = balance - %s WHERE id = %s"
                self.db.execute_query(update_query, (amount, account_id))

                ctk.CTkLabel(self.main_area, text=f"Retrait de {amount:.2f} € effectué ✅", text_color="green").pack(pady=10)
           except ValueError:
                ctk.CTkLabel(self.main_area, text="Veuillez entrer un montant valide.", text_color="red").pack()
           except Exception as e:
                print(f"[ERREUR RETRAIT] {e}")
                ctk.CTkLabel(self.main_area, text=f"Erreur : {e}", text_color="red").pack()

        ctk.CTkButton(self.main_area, text="Valider le retrait", command=submit_withdrawal).pack(pady=20)



    def show_transfer_view(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Transfert d'argent", font=("Arial", 18)).pack(pady=20)
        
        ctk.CTkLabel(self.main_area, text="Email du destinataire :").pack()
        recipient_email_entry = ctk.CTkEntry(self.main_area)
        recipient_email_entry.pack(pady=5)

        ctk.CTkLabel(self.main_area, text="Montant :").pack()
        amount_entry = ctk.CTkEntry(self.main_area, placeholder_text="Ex: 75.00")
        amount_entry.pack(pady=5)

        ctk.CTkLabel(self.main_area, text="Description :").pack()
        description_entry = ctk.CTkEntry(self.main_area)
        description_entry.pack(pady=5)

        ctk.CTkLabel(self.main_area, text="Catégorie :").pack()
        category_entry = ctk.CTkEntry(self.main_area)
        category_entry.pack(pady=5)

        def submit_transfer():
            recipient_email = recipient_email_entry.get()
            description = description_entry.get()
            category = category_entry.get()

            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Montant invalide")

                # Vérifier solde de l'utilisateur actuel
                result = self.db.execute_query("SELECT id, balance FROM accounts WHERE user_id = %s", (self.user_data["id"],))
                if not result:
                    ctk.CTkLabel(self.main_area, text="Compte non trouvé.", text_color="red").pack()
                    return
                sender_account_id, sender_balance = result[0]

                if sender_balance < amount:
                    ctk.CTkLabel(self.main_area, text="Solde insuffisant ❌", text_color="red").pack()
                    return

                # Récupérer ID du destinataire
                user_result = self.db.execute_query("SELECT id FROM users WHERE email = %s", (recipient_email,))
                if not user_result:
                    ctk.CTkLabel(self.main_area, text="Destinataire introuvable.", text_color="red").pack()
                    return
                recipient_user_id = user_result[0][0]

                account_result = self.db.execute_query("SELECT id FROM accounts WHERE user_id = %s", (recipient_user_id,))
                if not account_result:
                    ctk.CTkLabel(self.main_area, text="Compte du destinataire introuvable.", text_color="red").pack()
                    return
                recipient_account_id = account_result[0][0]

                # ✅ Insertion des transactions
                self.db.execute_query(
                    "INSERT INTO transactions (account_id, amount, description, category, transaction_type) VALUES (%s, %s, %s, %s, 'transfer')",
                    (sender_account_id, amount, description, category)
                )
                self.db.execute_query(
                    "INSERT INTO transactions (account_id, amount, description, category, transaction_type) VALUES (%s, %s, %s, %s, 'transfer-received')",
                    (recipient_account_id, amount, description, category)
                )

                # ✅ Mise à jour des soldes
                self.db.execute_query("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, sender_account_id))
                self.db.execute_query("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, recipient_account_id))

                ctk.CTkLabel(self.main_area, text=f"Transfert de {amount:.2f} € effectué ✅", text_color="green").pack(pady=10)

            except ValueError:
              ctk.CTkLabel(self.main_area, text="Montant invalide.", text_color="red").pack()
            except Exception as e:
              print(f"[ERREUR TRANSFERT] {e}")
              ctk.CTkLabel(self.main_area, text=f"Erreur : {e}", text_color="red").pack()

        ctk.CTkButton(self.main_area, text="Valider le transfert", command=submit_transfer).pack(pady=20)

    def show_history_view(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Historique des transactions", font=("Arial", 18)).pack(pady=10)

        # --- Filtres ---
        filter_frame = ctk.CTkFrame(self.main_area)
        filter_frame.pack(pady=10, padx=10)

        # Type
        type_label = ctk.CTkLabel(filter_frame, text="Type :")
        type_label.grid(row=0, column=0, padx=5)
        type_options = ["", "deposit", "withdrawal", "transfer", "transfer-received"]
        type_dropdown = ctk.CTkOptionMenu(filter_frame, values=type_options)
        type_dropdown.grid(row=0, column=1, padx=5)

        # Catégorie
        category_label = ctk.CTkLabel(filter_frame, text="Catégorie :")
        category_label.grid(row=0, column=2, padx=5)
        category_entry = ctk.CTkEntry(filter_frame)
        category_entry.grid(row=0, column=3, padx=5)

        # Date
        date_label = ctk.CTkLabel(filter_frame, text="Depuis (AAAA-MM-JJ) :")
        date_label.grid(row=0, column=4, padx=5)
        date_entry = ctk.CTkEntry(filter_frame)
        date_entry.grid(row=0, column=5, padx=5)

        # Montant min
        amount_label = ctk.CTkLabel(filter_frame, text="Montant Min :")
        amount_label.grid(row=0, column=6, padx=5)
        amount_entry = ctk.CTkEntry(filter_frame)
        amount_entry.grid(row=0, column=7, padx=5)

        # Zone des résultats
        table_container = ctk.CTkFrame(self.main_area)
        table_container.pack(padx=10, pady=10, fill="both", expand=True)

        def load_transactions():
            for widget in table_container.winfo_children():
                widget.destroy()

            result = self.db.execute_query("SELECT id FROM accounts WHERE user_id = %s", (self.user_data["id"],))
            if not result:
                ctk.CTkLabel(table_container, text="Compte introuvable.", text_color="red").pack()
                return
            account_id = result[0][0]

            base_query = "SELECT amount, transaction_type, description, category, transaction_date FROM transactions WHERE account_id = %s"
            conditions = []
            params = [account_id]

            ttype = type_dropdown.get()
            if ttype:
                conditions.append("transaction_type = %s")
                params.append(ttype)

            category = category_entry.get()
            if category:
                conditions.append("category LIKE %s")
                params.append(f"%{category}%")

            date_str = date_entry.get()
            if date_str:
                conditions.append("transaction_date >= %s")
                params.append(date_str)

            min_amount = amount_entry.get()
            if min_amount:
                try:
                    min_amount = float(min_amount)
                    conditions.append("amount >= %s")
                    params.append(min_amount)
                except:
                    pass

            if conditions:
                base_query += " AND " + " AND ".join(conditions)

            base_query += " ORDER BY transaction_date DESC"
            transactions = self.db.execute_query(base_query, tuple(params))

            if not transactions:
                ctk.CTkLabel(table_container, text="Aucune transaction trouvée.").pack()
                return

            headers = ["Date", "Type", "Montant", "Catégorie", "Description"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(table_container, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=5, pady=5, sticky="w")

            for row_index, trans in enumerate(transactions, start=1):
                amount, t_type, desc, cat, date = trans
                values = [
                    date.strftime("%Y-%m-%d %H:%M:%S"),
                    t_type.upper(),
                    f"{amount:.2f} €",
                    cat or "-",
                    desc or "-"
                ]
                for col_index, value in enumerate(values):
                    ctk.CTkLabel(table_container, text=value).grid(row=row_index, column=col_index, padx=5, pady=2, sticky="w")

        # Bouton rechercher
        search_btn = ctk.CTkButton(filter_frame, text="🔍 Rechercher", command=load_transactions)
        search_btn.grid(row=0, column=8, padx=10)

        # Charger les transactions au lancement
        load_transactions()

    
    def show_overview(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Vue globale du compte", font=("Arial", 22, "bold")).pack(pady=10)

        # Récupérer le compte
        result = self.db.execute_query("SELECT id, balance FROM accounts WHERE user_id = %s", (self.user_data["id"],))
        if not result:
            ctk.CTkLabel(self.main_area, text="Compte introuvable.", text_color="red").pack()
            return
        account_id, balance = result[0]

        # ✅ Solde actuel
        solde_color = "red" if balance < 0 else "green"
        ctk.CTkLabel(self.main_area, text=f"Solde actuel : {balance:.2f} €", text_color=solde_color, font=("Arial", 18)).pack(pady=10)

        # ✅ Total des dépenses du mois en cours
        from datetime import datetime
        now = datetime.now()
        month_start = now.strftime("%Y-%m-01")

        query = """
        SELECT SUM(amount) FROM transactions 
        WHERE account_id = %s AND transaction_type IN ('withdrawal', 'transfer') AND transaction_date >= %s
        """
        total_depenses = self.db.execute_query(query, (account_id, month_start))
        total_dep = total_depenses[0][0] if total_depenses[0][0] else 0.0

        ctk.CTkLabel(self.main_area, text=f"Dépenses ce mois : {total_dep:.2f} €", text_color="orange", font=("Arial", 16)).pack(pady=5)

        # ✅ Message d'alerte si découvert
        if balance < 0:
            ctk.CTkLabel(self.main_area, text="⚠️ Attention, vous êtes à découvert !", text_color="red").pack(pady=5)

        # 🔽 Zone Graphiques combinés
        graph_container = ctk.CTkFrame(self.main_area)
        graph_container.pack(pady=10, padx=10, fill="both", expand=True)

        query = """
        SELECT amount, transaction_date FROM transactions
        WHERE account_id = %s AND transaction_type IN ('withdrawal', 'transfer')
        """
        transactions = self.db.execute_query(query, (account_id,))
        monthly_data = defaultdict(float)

    
        for amount, date in transactions:
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            key = date.strftime("%Y-%m")
            monthly_data[key] += float(amount)

        months = sorted(monthly_data.keys())
        values = [monthly_data[m] for m in months]

        fig, axs = plt.subplots(1, 2, figsize=(10, 4))  # Bar + Pie côte à côte

        # Graphique barres
        axs[0].bar(months, values, color="skyblue")
        axs[0].set_title("Dépenses mensuelles")
        axs[0].tick_params(axis="x", rotation=45)

        # Graphique camembert par catégorie
        cat_data = defaultdict(float)
        cat_query = """
        SELECT category, amount FROM transactions
        WHERE account_id = %s AND transaction_type IN ('withdrawal', 'transfer')
        """
        cat_result = self.db.execute_query(cat_query, (account_id,))
        for cat, amt in cat_result:
            cat = cat or "Autre"
            cat_data[cat] += float(amt)

        labels = list(cat_data.keys())
        sizes = list(cat_data.values())
        if sizes:
            axs[1].pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
            axs[1].set_title("Dépenses par catégorie")
        else:
            axs[1].text(0.5, 0.5, "Aucune donnée", ha='center', va='center')
            axs[1].axis("off")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack()
    def quit_to_main(self):
        self.destroy()               # Ferme la fenêtre banquier
        self.master.deiconify()



