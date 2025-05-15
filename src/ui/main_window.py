from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget

from ui.widgets.week_histogram import WeekHistogram


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Learning App")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setStyleSheet("background-color: #0c1017;")
        screen = QApplication.primaryScreen()

        rect = screen.availableGeometry()
        self.setGeometry(int(rect.width() / 4), int(rect.height() / 4), 1024, 600)

        self.init_ui()

    def init_ui(self):
        button_names = [
            "Home",
            "Pomodoro",
            "Quiz",
            "Second Brain",
            "Incremental Reading",
            "Active Recall",
            "Spaced Repetition",
        ]
        for i in range(len(button_names)):
            btn = QPushButton(button_names[i], self)
            btn.setGeometry(0, 50 * i + 50, 175, 50)
            btn.setStyleSheet("background-color: #192125; color: white;")
        self.main_screen()

    def main_screen(self):
        lbl_week_activity = QLabel("This Week Activity", self)
        lbl_week_activity.setGeometry(250, 100, 200, 25)
        lbl_week_activity.setStyleSheet("color: white;")
        self.week_activity()

        lbl_overall_activity = QLabel("Overall Activity", self)
        lbl_overall_activity.setGeometry(250, 300, 200, 25)
        lbl_overall_activity.setStyleSheet("color: white;")
        self.overall_activity()

        lbl_todo = QLabel("To-Do list: ", self)
        lbl_todo.setGeometry(750, 100, 200, 25)
        lbl_todo.setStyleSheet("color: white;")
        self.to_do_list()

    def week_activity(self):
        week_data = [24, 3, 8, 2, 6, 15, 4]
        if hasattr(self, "week_widget"):
            self.week_widget.setParent(None)
        self.week_widget = WeekHistogram(parent=self, data=week_data)
        self.week_widget.setGeometry(250, 130, 250, 125)

    def overall_activity(self):
        print("o")

    def to_do_list(self):
        print("t")
