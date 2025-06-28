import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from core.register import Register

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


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
