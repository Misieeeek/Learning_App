import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

from core.auto_login import Auto_Login
from core.database_manager import Database_Manager
from core.login import Login
from core.register import Register

# from core.todo_repository import Todo
from core.user_activity import User_Activity
from ui.main_window_ui import Ui_Form
from ui.widgets.home_widget import Home_Widget
from ui.widgets.quiz_widget import Quiz_Widget  

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        for btn in self.findChildren(QPushButton):
            method_name = f"on_{btn.objectName()}_pressed"
            if hasattr(self, method_name):
                btn.clicked.connect(getattr(self, method_name))

        self.login_menu = self.ui.login_menu
        self.logged_in_widget = self.ui.logged_in_widget
        self.logged_out_widget = self.ui.logged_out_widget
        self.main_widget = self.ui.main_widget
        self.home_widget = self.ui.home_widget
        self.sign_up_in_widget = self.ui.sign_up_in_widget

        self.db_manager = Database_Manager()
        self.db_manager.create_tables()

        self.home_widget_controller = Home_Widget(self)
        self.activity_controller = User_Activity()
        self.quiz_widget_controller = Quiz_Widget(self)

        # self.todo_widget_controller = Todo()
        self.username = None
        self.remember = Auto_Login()
        self.login_status()

    def on_sign_up_btn_pressed(self):
        username = self.ui.username_up_input.text()
        password = self.ui.password_up_input.text()
        confirm_password = self.ui.confirm_password_input.text()
        new_user = Register(username, password, confirm_password, parent=self)
        new_user.register_user()

    def on_home_btn_pressed(self):
        if self.username:
            self.main_widget.setCurrentWidget(self.home_widget)
            self.home_widget_controller.change_screen_home(self.username)
    
    def on_to_do_btn_pressed(self):
        if self.username:
            self.main_widget.setCurrentWidget(self.ui.todo_widget)
    
    def on_pomodoro_btn_pressed(self):
        if self.username:
            self.main_widget.setCurrentWidget(self.ui.pomodoro_widget)
    
    def on_quiz_btn_pressed(self):
        if self.username:
            self.main_widget.setCurrentWidget(self.ui.quiz_widget)
    
    def on_second_brain_btn_pressed(self):
        if self.username:
            self.main_widget.setCurrentWidget(self.ui.second_brain_widget)
    
    def on_incremental_reading_btn_pressed(self):
        if self.username:
            self.main_widget.setCurrentWidget(self.ui.incremental_reading_widget)
    
    def on_active_recall_btn_pressed(self):
        if self.username:
            self.main_widget.setCurrentWidget(self.ui.active_recall_widget)
    
    def on_spaced_repetition_btn_pressed(self):
        if self.username:
            self.main_widget.setCurrentWidget(self.ui.spaced_repetition_widget)

    def on_sign_in_btn_pressed(self):
        username = self.ui.username_in_input.text()
        password = self.ui.password_in_input.text()
        user = Login(username, password, parent=self)
        if user.login():
            if self.ui.stay_logged_cb.isChecked():
                self.remember.save_logged_in_out_user(username)
            else:
                self.remember.save_logged_in_out_user()

            self.username = username
            self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.main_widget.setCurrentWidget(self.home_widget)
            self.login_menu.setCurrentWidget(self.logged_in_widget)
            self.home_widget_controller.change_screen_home(self.username)

    def on_log_out_btn_pressed(self):
        start_time = self.start_time
        self.activity_controller.save_activity(
            self.username, start_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.remember.save_logged_in_out_user()
        self.home_widget_controller.change_screen_sign_up_in()

    def login_status(self):
        self.username = self.remember.load_logged_user()
        if self.username is None:
            self.home_widget_controller.change_screen_sign_up_in()
        else:
            self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.home_widget_controller.change_screen_home(self.username)

    def closeEvent(self, event):
        if self.username:
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.activity_controller.save_activity(
                self.username, self.start_time, end_time
            )

        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = Main_Window()
    window.show()
    sys.exit(app.exec())
