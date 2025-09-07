from datetime import datetime

from PyQt6.QtCore import QRect
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QToolTip, QWidget


class Week_Histogram(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = [0.0] * 7
        if isinstance(data, dict):
            for date_str, value in data.items():
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                index = dt.weekday()
                self.data[index] += float(value)

        self.setMouseTracking(True)
        self.hovered_index = None
        self.labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.border_opacity = 150
        self.border_direction = 1
        self.show()

    def paintEvent(self, event):
        if not self.data:
            return

        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        bar_width = self.width() // len(self.data)
        max_h = max(self.data) or 1

        if max_h == 0:
            max_h = 1

        font = QFont()
        font.setPointSize(10)
        qp.setFont(font)

        for i, value in enumerate(self.data):
            x = i * bar_width
            height = int((value / max_h) * (self.height() - 40))
            y = self.height() - height - 20

            ratio = value / max_h
            fill_color = QColor(0, int(255 * ratio), 0)

            brush = QBrush(fill_color)

            if i == self.hovered_index:
                pen_color = QColor(0, 128, 240, self.border_opacity)
            else:
                pen_color = QColor(255, 255, 255, 150)

            pen = QPen(pen_color)
            pen.setWidth(2)

            qp.setBrush(brush)
            qp.setPen(pen)
            qp.drawRect(QRect(x + 5, y, bar_width - 10, height))

            label = self.labels[i % len(self.labels)]
            text_x = x + (bar_width // 2) - 10
            qp.setPen(QColor("white"))
            qp.drawText(text_x, self.height() - 5, label)
        qp.end()

    def mouseMoveEvent(self, event):
        if not self.data:
            return super().mouseMoveEvent(event)

        bar_width = self.width() // len(self.data)
        idx = event.x() // bar_width

        if 0 <= idx < len(self.data):
            max_h = max(self.data) or 1
            bar_height = int((self.data[idx] / max_h) * (self.height() - 40))
            bar_top_y = self.height() - bar_height - 20

            if event.y() >= bar_top_y:
                if idx != self.hovered_index:
                    self.hovered_index = idx
                    QToolTip.showText(
                        self.mapToGlobal(event.pos()),
                        f"Time spent: {round(self.data[idx], 2)} hours",
                        self,
                    )
                    self.setStyleSheet("""
                        QToolTip { 
                            background-color: #3b434d; 
                            color: white;
                            border-radius: 25px;
                            padding: 5px;
                        }
                    """)
                    self.update()
                return

        if self.hovered_index is not None:
            self.hovered_index = None
            QToolTip.hideText()
            self.update()

        return super().mouseMoveEvent(event)
