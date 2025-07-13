from PyQt5.QtWidgets import QVBoxLayout, QWidget

from ui.widgets.overall_activity import Overall_Activity
from ui.widgets.week_histogram import Week_Histogram


class Home_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.week_widget = None
        self.overall_activity = None

    def change_screen_home(self):
        self.parent.login_menu.setCurrentWidget(self.parent.logged_in_widget)
        self.parent.main_widget.setCurrentWidget(self.parent.home_widget)

        # remove and change to database info
        week_data = [24, 3, 8, 2, 6, 15, 4]
        activity_data = [1, 2, 3, 4, 5, 6, 7] * 12

        waw_container = self.parent.home_widget.findChild(
            QWidget, "week_activity_widget"
        )
        oaw_container = self.parent.home_widget.findChild(
            QWidget, "overall_activity_widget"
        )

        if waw_container.layout() is None and oaw_container.layout() is None:
            waw_container.setLayout(QVBoxLayout())
            oaw_container.setLayout(QVBoxLayout())

        waw_layout = waw_container.layout()
        oaw_layout = oaw_container.layout()

        if (
            hasattr(self, "week_widget")
            and self.week_widget
            and hasattr(self, "overall_activity")
            and self.overall_activity
        ):
            waw_layout.removeWidget(self.week_widget)
            self.week_widget.deleteLater()
            oaw_layout.removeWidget(self.overall_activity)
            self.overall_activity.deleteLater()

        self.week_widget = Week_Histogram(parent=waw_container, data=week_data)
        waw_layout.addWidget(self.week_widget)

        self.overall_activity = Overall_Activity(
            parent=oaw_container, data=activity_data
        )
        oaw_layout.addWidget(self.overall_activity)

    def change_screen_sign_up_in(self):
        self.parent.login_menu.setCurrentWidget(self.parent.logged_out_widget)
        self.parent.main_widget.setCurrentWidget(self.parent.sign_up_in_widget)
