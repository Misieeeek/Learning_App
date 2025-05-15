from PyQt5.QtCore import QRect
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QToolTip, QWidget


class WeekHistogram(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data or []
        self.setMouseTracking(True)
        self.hovered_index = None
        self.show()

    def paintEvent(self, event):
        if not self.data:
            return

        qp = QPainter(self)
        bar_width = self.width() // len(self.data)
        max_h = max(self.data)

        lbls = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        for i, value in enumerate(self.data):
            x = i * bar_width
            height = int((value / max_h) * (self.height() - 20))
            y = self.height() - height

            ratio = value / max_h
            color = QColor(0, int(255 * (ratio)), 0)

            brush = QBrush(color)
            pen = QPen(QColor(255, 255, 255, 150))
            pen.setWidth(2)

            qp.setBrush(brush)
            qp.setPen(pen)
            qp.drawRect(QRect(x + 5, y, bar_width - 10, height))

            # lbl

    def mouseMoveEvent(self, event):
        if not self.data:
            return super().mouseMoveEvent(event)

        bar_width = self.width() // len(self.data)
        idx = event.x() // bar_width

        if 0 <= idx < len(self.data):
            if idx != self.hovered_index:
                self.hovered_index = idx
                QToolTip.showText(
                    self.mapToGlobal(event.pos()),
                    f"Time spent: {self.data[idx]} hours",
                    self,
                )
                self.setStyleSheet("""QToolTip { 
                           background-color: #3b434d; 
                           color: white;
                           border-radius: 25px;
                           }""")
        else:
            if self.hovered_index is not None:
                self.hovered_index = None
                QToolTip.hideText()
                self.update()

        return super().mouseMoveEvent(event)
