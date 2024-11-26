class UserDTO:
    def __init__(self, user_id, username, password, email=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email  # Додати email у відповідь, якщо потрібно
        }
