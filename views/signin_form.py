import customtkinter as ctk
import bcrypt
import re
from db.database import *
from views.my_account_window import MyAccountWindow


class SignInForm(ctk.CTk):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.title("User Sign In Form")
        self.geometry("600x500")
        self.resizable(False, False)

        # Form Title
        self.title_label = ctk.CTkLabel(self, text="Sign-in", font=("Arial", 24))
        self.title_label.grid(row=0, column=1, pady=10)

        # Email
        self.email_label = ctk.CTkLabel(self, text="Email:")
        self.email_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.email_entry = ctk.CTkEntry(self, width=250)
        self.email_entry.grid(row=3, column=1, padx=20, pady=10)

        # Password
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(self, width=250, show="*")
        self.password_entry.grid(row=4, column=1, padx=20, pady=10)

        # Sign-in Button
        self.register_button = ctk.CTkButton(self, text="Sign-in", command=self.signin)
        self.register_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Status label for messages
        self.status_label = ctk.CTkLabel(self, text="", text_color="red", wraplength=350)
        self.status_label.grid(row=8, column=0, columnspan=2)

    def signin(self):
        # Retrieve the input values
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if email and password are provided
        if not email or not password:
            self.status_label.configure(text="Please provide both email and password.")
            return

        # Check if the email exists in the database
        user_data = self.db.get_user_by_email(email)
        if user_data is None:
            self.status_label.configure(text="Email not found. Please check your email.")
            return

        # Check if the provided password matches the hashed password in the database
        hashed_password = self.db.get_hashed_password(email)
        if not hashed_password:
            self.status_label.configure(text="Email not found in the database.")
            return
        # Check if the provided password matches the hashed password
        if not self.db.verify_password(password, hashed_password):
            self.status_label.configure(text="Incorrect password.")
            return
        
        
        """ # Check if the password matches
        hashed_password = user_data["password"]
        if not self.check_password(password, hashed_password):
            self.status_label.configure(text="Incorrect password. Please try again.")
            return"""
        
        # Check if the password matches the hashed password
        if not self.db.verify_password(password, hashed_password):
            self.status_label.configure(text="Incorrect password. Please try again.")
            return

        
        # Success, user can sign in
        self.status_label.configure(text="Welcome back! You're signed in successfully.", text_color="green")
        # Optionally, close the login window if needed
        self.after(2000, self.destroy)

        # Open the "My Account" window and Pass the email
        self.open_my_account_window(email)


    def open_my_account_window(self, email):
        # Suppose MyAccountWindow is your next window after login
        my_account_window = MyAccountWindow(self.db, email)

    """def check_password(self, password, hashed_password):
        # Check if the password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))"""

       

