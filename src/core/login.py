from PyQt5.QtWidgets import QMessageBox

from core.user_repository import User_Repository


class Login:
    def __init__(self, username, password, parent=None):
        self.username = username
        self.password = password
        self.parent = parent

    def login(self):
        if not self.username or not self.password:
            QMessageBox.warning(self.parent, "Error", "All fields must be filled in")
            return

        db = User_Repository()
        verified = db.verify_user(self.username, self.password)
        if verified:
            print("Password correct")
        else:
            QMessageBox.warning(
                self.parent, "Error", "User not found or password is incorrect"
            )
