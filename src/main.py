import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from core.password_hasher import Password_Hasher
from core.register import Register
from core.user_repository import User_Repository

ui_file = os.path.join(os.path.dirname(__file__), "ui", "main_window.ui")
wnd, cls = uic.loadUiType(ui_file)


class MainWindow(wnd, cls):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def on_sign_up_btn_pressed(self):
        username = self.username_up_input.text()
        password = self.password_up_input.text()
        confirm_password = self.confirm_password_input.text()
        new_user = Register(username, password, confirm_password)
        new_user.register_user()

    def on_sign_in_btn_pressed(self):
        username = self.username_in_input.text()
        password = self.password_in_input.text()

        if username == "" or password == "":
            print("Need username and/or password")
            return

        db = User_Repository()
        db_password = db.get_user_password(username)

        ph = Password_Hasher()

        if ph.verify(password, db_password[0]):
            print("Pass correct")
        else:
            print("Pass incorrect")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
