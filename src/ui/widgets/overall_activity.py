import datetime

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QToolTip, QWidget


class Overall_Activity(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.hovered_pos = None
        self.cell_size = 9
        self.spacing = 3
        self.top_padding = 25
        self.left_padding = 35

        self.year = datetime.date.today().year
        self.data = data or []
        self.processed_data = self._process_data()

        total_weeks = (len(self.processed_data) + 6) // 7
        self.setMinimumHeight(self.cell_size * 7 + self.top_padding + 10)
        self.setMinimumWidth(self.cell_size * (total_weeks + 2) + self.left_padding)
        self.show()

    def _process_data(self):
        start_day = datetime.date(self.year, 1, 1)
        end_day = datetime.date(self.year, 12, 31)
        total_days = (end_day - start_day).days + 1

        padded_data = self.data[:total_days]
        if len(padded_data) < total_days:
            padded_data += [0] * (total_days - len(padded_data))

        full_data = []
        for i in range(total_days):
            date = start_day + datetime.timedelta(days=i)
            full_data.append((date, padded_data[i]))

        return full_data

    def paintEvent(self, event):
        if not self.processed_data:
            return

        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        max_val = max(self.data or [1])

        font = QFont()
        font.setPointSize(8)
        qp.setFont(font)

        days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, label in enumerate(days_labels):
            qp.setPen(Qt.white)
            y = self.top_padding + i * (self.cell_size + self.spacing) + 10
            qp.drawText(2, y, label)

        last_month = None
        column = 0

        jan_first = datetime.date(self.year, 1, 1)
        start_day = jan_first - datetime.timedelta(days=jan_first.weekday())

        for i in range(len(self.processed_data)):
            date, value = self.processed_data[i]
            days_from_start = (date - start_day).days
            col = days_from_start // 7
            row = date.weekday()

            x = self.left_padding + col * (self.cell_size + self.spacing)
            y = self.top_padding + row * (self.cell_size + self.spacing)

            if date.day == 1 or (last_month != date.month and row == 0):
                month_label = date.strftime("%b")
                qp.setPen(Qt.white)
                qp.drawText(x, 10, month_label)
                last_month = date.month

            ratio = value / max_val if max_val else 0
            color = self._get_color(ratio)
            qp.setBrush(QBrush(color))

            if value == 0:
                pen = QPen(QColor(100, 100, 100, 150))
            else:
                pen = QPen(QColor(40, 40, 40))
            pen.setWidth(1)
            qp.setPen(pen)

            qp.drawRect(QRect(x, y, self.cell_size, self.cell_size))

    def _get_color(self, ratio):
        if ratio == 0:
            return QColor("#2c2f33")
        elif ratio < 0.25:
            return QColor("#0e4429")
        elif ratio < 0.5:
            return QColor("#006d32")
        elif ratio < 0.75:
            return QColor("#26a641")
        else:
            return QColor("#39d353")

    def mouseMoveEvent(self, event):
        if not self.processed_data:
            return super().mouseMoveEvent(event)

        pos = event.pos()
        jan_first = datetime.date(self.year, 1, 1)
        start_day = jan_first - datetime.timedelta(days=jan_first.weekday())

        for i, (date, value) in enumerate(self.processed_data):
            days_from_start = (date - start_day).days
            col = days_from_start // 7
            row = date.weekday()

            x = self.left_padding + col * (self.cell_size + self.spacing)
            y = self.top_padding + row * (self.cell_size + self.spacing)

            cell_rect = QRect(x, y, self.cell_size, self.cell_size)

            if cell_rect.contains(pos):
                tooltip_text = f"{date.strftime('%A, %b %d %Y')}\n{value} hour(s) spent"
                QToolTip.showText(
                    self.mapToGlobal(pos),
                    tooltip_text,
                    self,
                )
                self.setStyleSheet("""
                    QToolTip { 
                        background-color: #3b434d; 
                        color: white;
                        border-radius: 5px;
                        padding: 5px;
                    }
                """)
                return

        QToolTip.hideText()
        return super().mouseMoveEvent(event)
