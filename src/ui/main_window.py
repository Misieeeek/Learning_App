from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Learning App")
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        screen = QApplication.primaryScreen()
        screen_size = screen.size()

        rect = screen.availableGeometry()
        self.setGeometry(int(rect.width() / 4), int(rect.height() / 4), 1024, 600)
