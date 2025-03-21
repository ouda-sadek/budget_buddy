import customtkinter as ctk
import re
import bcrypt
from db.database import *

class RegistrationForm(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        
        self.db = db
        self.title("User Registration Form")
        self.geometry("600x500")
        self.resizable(False, False)

        # Form Title
        self.title_label = ctk.CTkLabel(self, text="Register", font=("Arial", 24))
        self.title_label.grid(row=0, column=1, pady=10)

        # First Name
        self.first_name_label = ctk.CTkLabel(self, text="First Name:")
        self.first_name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.first_name_entry = ctk.CTkEntry(self, width=250)
        self.first_name_entry.grid(row=1, column=1, padx=20, pady=10)

        # Last Name
        self.last_name_label = ctk.CTkLabel(self, text="Last Name:")
        self.last_name_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.last_name_entry = ctk.CTkEntry(self, width=250)
        self.last_name_entry.grid(row=2, column=1, padx=20, pady=10)

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

        # Confirm password
        self.confirm_password_label = ctk.CTkLabel(self, text="Confirm Password:")
        self.confirm_password_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.confirm_password_entry = ctk.CTkEntry(self, width=250, show="*")
        self.confirm_password_entry.grid(row=5, column=1, padx=20, pady=10)

        # Register Button
        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Status label for messages
        self.status_label = ctk.CTkLabel(self, text="", text_color="red", wraplength=350)
        self.status_label.grid(row=7, column=0, columnspan=2)

        

    def register(self):
        # Retrieve the input values
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        

        # Validate email format
        if not self.is_valid_email(email):
            self.status_label.configure(text="Invalid email format")
            return
        
        # Check if email already exists
        if self.db.email_exists(email):
            self.status_label.configure(text="Email already exists, please use a different email.")
            return


        # Validate password
        if not self.is_valid_password(password):
            self.status_label.configure(text="Password must contain at least one uppercase letter, one lowercase letter, one digit, one special character, and be at least 10 characters long.")
            return
        
        # Check if password and confirm password match
        if password != confirm_password:
            self.status_label.configure(text="Passwords do not match. Please make sure both passwords are the same.")
            return
        
        # Hash the password before saving to the database
        hashed_password = self.hash_password(password)
        print(f"Hashed password: {hashed_password}")

        # Insert user data into the database
        if self.db.insert_user_data(first_name, last_name, email, hashed_password):
            # Display success message
            self.status_label.configure(text=f"Welcome {first_name} {last_name}, you are registered successfully!", text_color="green")
            self.after(2000, self.destroy)
        else:
            self.status_label.configure(text="An error occurred while saving your data. Please try again.")

        

        
    def is_valid_email(self, email):
        # Validate email using regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def is_valid_password(self, password):
        # Validate password complexity
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{10,}$'
        return re.match(password_regex, password) is not None
    
    def hash_password(self, password):
        # Hash the password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    


"""if __name__ == "__main__":
    app = RegistrationForm()
    app.mainloop()"""

