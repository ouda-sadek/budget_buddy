import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageEnhance
import os
from user import UserManager  

ctk.set_appearance_mode("Dark")

class BudgetBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("800x600")
        self.resizable(False, False)

        self.user_manager = UserManager()

        image_path = os.path.join("budget_buddy", "images", "DNR.jpg")
        self.bg_image_original = None  # Initialiser l'attribut
        self.set_background_image(image_path)

        # Calque semi-transparent (caché par défaut)
        self.overlay = ctk.CTkLabel(self, text="", fg_color="black", width=800, height=600)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lower()  # Toujours en arrière-plan

        self.create_main_buttons()

    def set_background_image(self, image_path):
        """Charge l'image de fond et la stocke"""
        try:
            if os.path.exists(image_path):
                self.bg_image_original = Image.open(image_path)  # Stocke l'image originale
                self.bg_photo = ctk.CTkImage(self.bg_image_original, size=(800, 600))

                self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
                self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
            else:
                print(f"Background image not found at location: {image_path}")
        except Exception as e:
            print(f"Error loading image: {e}")

    def darken_background(self, darken=True):
        """Assombrit ou restaure le background"""
        if self.bg_image_original is None:
            print("Avertissement : L'image de fond n'est pas chargée.")
            return

        if darken:
            enhancer = ImageEnhance.Brightness(self.bg_image_original)
            darkened_image = enhancer.enhance(0.3)  # Réduit la luminosité à 50%
            self.bg_photo = ctk.CTkImage(darkened_image, size=(800, 600))
        else:
            self.bg_photo = ctk.CTkImage(self.bg_image_original, size=(800, 600))  # Restaure l'image originale

        # Met à jour l'image affichée
        self.bg_label.configure(image=self.bg_photo)

    def clear_widgets(self):
        """Supprime tous les widgets SAUF l'image de fond"""
        for widget in self.winfo_children():
            if widget not in [self.bg_label, self.overlay]:  # Garde l'image et le calque
                widget.destroy()

    def create_main_buttons(self):
        """Affiche les boutons principaux et enlève l'effet d'assombrissement"""
        self.clear_widgets()
        self.darken_background(False)  # Supprime l'effet sombre

        self.login_button = ctk.CTkButton(self, text="Login", command=self.show_login_screen, width=200, height=50, fg_color="#669966")
        self.login_button.place(x=170, y=450)

        self.signup_button = ctk.CTkButton(self, text="Signup", command=self.show_signup_screen, width=200, height=50, fg_color="#669966")
        self.signup_button.place(x=450, y=450)

    def show_login_screen(self):
        """Affiche le formulaire de connexion et assombrit le fond"""
        self.clear_widgets()
        self.darken_background(True)  # Active l'effet sombre

        ctk.CTkLabel(self, text="Email:").pack(pady=5)
        email_entry = ctk.CTkEntry(self)
        email_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Mot de passe:").pack(pady=5)
        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack(pady=5)

        def login():
            email = email_entry.get()
            password = password_entry.get()
            success, user_data = self.user_manager.login_user(email, password)
            if success:
                messagebox.showinfo("Succès", f"Bienvenue {user_data['first_name']} !")
                self.create_main_buttons()  # Retour au menu principal
            else:
                messagebox.showerror("Erreur", user_data)

        ctk.CTkButton(self, text="Se connecter", command=login).pack(pady=10)
        ctk.CTkButton(self, text="Retour", command=self.create_main_buttons).pack(pady=5)

    def show_signup_screen(self):
        """Affiche le formulaire d'inscription et assombrit le fond"""
        self.clear_widgets()
        self.darken_background(True)  # Active l'effet sombre

        ctk.CTkLabel(self, text="Prénom:").pack(pady=5)
        first_name_entry = ctk.CTkEntry(self)
        first_name_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Nom:").pack(pady=5)
        last_name_entry = ctk.CTkEntry(self)
        last_name_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Email:").pack(pady=5)
        email_entry = ctk.CTkEntry(self)
        email_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Mot de passe:").pack(pady=5)
        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack(pady=5)

        def signup():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            success, message = self.user_manager.register_user(first_name, last_name, email, password)
            if success:
                messagebox.showinfo("Succès", message)
                self.create_main_buttons()  # Retour au menu principal
            else:
                messagebox.showerror("Erreur", message)

        ctk.CTkButton(self, text="S'inscrire", command=signup).pack(pady=10)
        ctk.CTkButton(self, text="Retour", command=self.create_main_buttons).pack(pady=5)

# Lancer l’application
if __name__ == "__main__":
    app = BudgetBuddyApp()
    app.mainloop()