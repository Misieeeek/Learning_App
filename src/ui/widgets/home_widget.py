from PyQt5.QtWidgets import QVBoxLayout, QWidget

from ui.widgets.week_histogram import Week_Histogram


class Home_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.week_widget = None

    def change_screen_home(self):
        self.parent.login_menu.setCurrentWidget(self.parent.logged_in_widget)
        self.parent.main_widget.setCurrentWidget(self.parent.home_widget)

        week_data = [24, 3, 8, 2, 6, 15, 4]

        container = self.parent.home_widget.findChild(QWidget, "week_activity_widget")

        if container.layout() is None:
            container.setLayout(QVBoxLayout())

        layout = container.layout()

        if hasattr(self, "week_widget") and self.week_widget:
            layout.removeWidget(self.week_widget)
            self.week_widget.deleteLater()

        self.week_widget = Week_Histogram(parent=container, data=week_data)
        layout.addWidget(self.week_widget)

    def change_screen_sign_up_in(self):
        self.parent.login_menu.setCurrentWidget(self.parent.logged_out_widget)
        self.parent.main_widget.setCurrentWidget(self.parent.sign_up_in_widget)
