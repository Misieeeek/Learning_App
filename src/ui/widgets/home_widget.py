from datetime import datetime

from PyQt5.QtWidgets import QVBoxLayout, QWidget

from core.auto_login import Auto_Login
from core.user_activity import User_Activity
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

        al = Auto_Login()
        username = al.load_logged_user()

        ua = User_Activity()
        user_id = ua.get_user_id(username)
        today_date = datetime.now()
        week_data = ua.get_user_week_activity(user_id, today_date)

        activity_data = ua.get_user_year_activity(user_id)

        waw_container = self.parent.home_widget.findChild(
            QWidget, "week_activity_widget"
        )
        oaw_container = self.parent.home_widget.findChild(
            QWidget, "overall_activity_widget"
        )

        if waw_container.layout() is None:
            waw_container.setLayout(QVBoxLayout())
        if oaw_container.layout() is None:
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
        self.cleanup_home_widgets()
        self.parent.login_menu.setCurrentWidget(self.parent.logged_out_widget)
        self.parent.main_widget.setCurrentWidget(self.parent.sign_up_in_widget)

    def clear_layout(self, layout):  # POPRAWKA: dodane 'self'
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def cleanup_home_widgets(self):
        """Czyści widgety domowe przed zmianą ekranu"""
        waw_container = self.parent.home_widget.findChild(
            QWidget, "week_activity_widget"
        )
        oaw_container = self.parent.home_widget.findChild(
            QWidget, "overall_activity_widget"
        )

        if waw_container and waw_container.layout():
            self.clear_layout(waw_container.layout())

        if oaw_container and oaw_container.layout():
            self.clear_layout(oaw_container.layout())

        self.week_widget = None
        self.overall_activity = None
