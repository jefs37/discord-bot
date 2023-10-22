class UserData:
    def __init__(self, user_id, username, balance):
        self.user_id = user_id
        self.username = username
        self.balance = balance

    def __str__(self):
            return f"User ID: {self.user_id}, Username: {self.username}, Balance: {self.balance}"