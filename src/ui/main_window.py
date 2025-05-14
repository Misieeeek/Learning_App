from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Learning App")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setStyleSheet("background-color: black;")
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
            btn.setStyleSheet("background-color: #1a1a1a; color: white;")
