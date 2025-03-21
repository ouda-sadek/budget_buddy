import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from views.signup_form import *
from views.signin_form import *
#from db.database import *   

# Appearance configuration
ctk.set_appearance_mode("Dark")


class BudgetBuddyApp(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Budget Buddy")
        self.geometry("800x600")
        self.resizable(False, False)

        # Relative path to the image
        image_path = os.path.join("budget_buddy", "images", "DNR.jpg")
        self.set_background_image(image_path)

        # Creating widgets
        self.create_widgets()

    def set_background_image(self, image_path):
      
      try:
        if os.path.exists(image_path):
           # Load the image with PIL
            self.bg_image = Image.open(image_path)
            
           # Resize the image to fit the window
            self.bg_photo = ctk.CTkImage(self.bg_image, size=(800, 600))

            # Display the image in a label that covers the entire window
            self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
            self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            print(f"Background image not found at location : {image_path}")
      except Exception as e:
        print(f"Error loading image : {e}")

    def create_widgets(self):
        # Button to connect
        self.login_button = ctk.CTkButton(
            self,
            text="Login",
            command=self.open_signin_form,
            width=200,
            height=50,
            fg_color="#669966",
            hover_color="darkgray",  
            text_color="white",  
        )
        self.login_button.place(x=170, y=450)

        # Button to register
        self.signup_button = ctk.CTkButton(
            self,
            text="Signup",
            command=self.open_signup_form,
            width=200,
            height=50,
            fg_color="#669966",
            hover_color="darkgray",  
            text_color="white",  
        )
        self.signup_button.place(x=450, y=450)

    def login(self):
        messagebox.showinfo("Login", "Login button clicked")

    def signup(self):
        messagebox.showinfo("Signup", "Signup button clicked")

    def open_signup_form(self):
       signup_form = RegistrationForm (self.db)
       #signup_form.grab_set()

    def open_signin_form(self):
       signin_form = SignInForm (self.db)
# Application entry point
"""if __name__ == "__main__":
    app = BudgetBuddyApp()
    app.mainloop()"""