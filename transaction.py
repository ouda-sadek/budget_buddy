from db.database import Database

class TransactionManager:
    def __init__(self, user_id):
        self.db = Database()
        self.user_id = user_id

    def add_transaction(self, reference, description, montant, date, type):
        self.db.add_transaction(self.user_id, reference, description, montant, date, type)

    def get_transactions(self):
        return self.db.get_transactions(self.user_id)