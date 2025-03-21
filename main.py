from db.database import Database
from views.main_window import BudgetBuddyApp                                                                         
#from gui import *


def main():
    db = Database(host="localhost", user="root", password="", database="budget_buddy")
    app = BudgetBuddyApp(db)
    
    
    app.mainloop()

if __name__ == "__main__":
     main()

