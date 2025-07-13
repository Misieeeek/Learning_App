import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from core.auto_login import Auto_Login
from core.login import Login
from core.register import Register
from ui.widgets.home_widget import Home_Widget

ui_file = os.path.join(os.path.dirname(__file__), "ui", "main_window.ui")
wnd, cls = uic.loadUiType(ui_file)


class Main_Window(wnd, cls):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.home_widget_controller = Home_Widget(self)
        self.login_status()

    def on_sign_up_btn_pressed(self):
        username = self.username_up_input.text()
        password = self.password_up_input.text()
        confirm_password = self.confirm_password_input.text()
        new_user = Register(username, password, confirm_password, parent=self)
        new_user.register_user()

    def on_sign_in_btn_pressed(self):
        username = self.username_in_input.text()
        password = self.password_in_input.text()
        user = Login(username, password, parent=self)
        if user.login():
            remember = Auto_Login()
            if self.stay_logged_cb.isChecked():
                remember.save_logged_in_out_user(username)
            else:
                remember.save_logged_in_out_user()
            self.main_widget.setCurrentWidget(self.home_widget)
            self.login_menu.setCurrentWidget(self.logged_in_widget)
            self.home_widget_controller.change_screen_home()

    def on_log_out_btn_pressed(self):
        remember = Auto_Login()
        remember.save_logged_in_out_user()
        self.home_widget_controller.change_screen_sign_up_in()

    def login_status(self):
        user = Auto_Login()
        username = user.load_logged_user()
        if username is None:
            self.home_widget_controller.change_screen_sign_up_in()
        else:
            self.home_widget_controller.change_screen_home()


if __name__ == "__main__":
    app = QApplication([])
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
