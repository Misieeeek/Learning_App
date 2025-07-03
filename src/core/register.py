from PyQt5.QtWidgets import QMessageBox

from core.user_repository import User_Repository


class Register:
    def __init__(self, username, password, confirm_password, parent=None):
        self.username = username
        self.password = password
        self.confirm_password = confirm_password
        self.parent = parent

    def register_user(self):
        can_register = self.input_correct()
        if can_register:
            user_repo = User_Repository()
            user_repo.save_user(self.username, self.password)
        else:
            QMessageBox.warning(
                self.parent,
                "Error",
                "All fields must be filled in, make sure password match",
            )

    def input_correct(self):
        if (
            not self.username
            or not self.password
            or not self.confirm_password
            or self.password != self.confirm_password
        ):
            return False
        return True
