from PyQt5.QtWidgets import QMainWindow
from ui_main_window import Ui_Form


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def init_ui(self):
        self.main_screen()

    def main_screen(self):
        self.to_do_list()

    def week_activity(self):
        week_data = [24, 3, 8, 2, 6, 15, 4]
        # if hasattr(self, "week_widget"):
        #     self.week_widget.setParent(None)
        # self.week_widget = WeekHistogram(parent=self, data=week_data)
        # self.week_widget.setGeometry(250, 130, 250, 125)

    def overall_activity(self):
        print("o")

    def to_do_list(self):
        print("t")
