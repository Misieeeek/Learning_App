import os
import sys
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from core.auto_login import Auto_Login
from core.login import Login
from core.register import Register
from core.user_activity import User_Activity
from ui.widgets.home_widget import Home_Widget

ui_file = os.path.join(os.path.dirname(__file__), "ui", "main_window.ui")
wnd, cls = uic.loadUiType(ui_file)


class Main_Window(wnd, cls):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.home_widget_controller = Home_Widget(self)
        self.activity_controller = User_Activity()
        self.remember = Auto_Login()
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
            self.activity_controller.create_activity_table()
            if self.stay_logged_cb.isChecked():
                self.remember.save_logged_in_out_user(username)
            else:
                self.remember.save_logged_in_out_user()
            self.activity_controller.save_activity(
                username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            self.main_widget.setCurrentWidget(self.home_widget)
            self.login_menu.setCurrentWidget(self.logged_in_widget)
            self.home_widget_controller.change_screen_home()

    def on_log_out_btn_pressed(self):
        self.record_activity.stop_and_save_recording()
        username = self.remember.load_logged_user()
        self.activity_controller.save_activity(
            username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.remember.save_logged_in_out_user()
        self.home_widget_controller.change_screen_sign_up_in()

    def login_status(self):
        username = self.remember.load_logged_user()
        if username is None:
            self.home_widget_controller.change_screen_sign_up_in()
        else:
            self.activity_controller.save_activity(
                username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            self.home_widget_controller.change_screen_home()


if __name__ == "__main__":
    app = QApplication([])
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
