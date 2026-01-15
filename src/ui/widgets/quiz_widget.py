import os

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QFileDialog, QWidget


class Quiz_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.max_recent_files = 5

        self.settings = QSettings("LearningApp", "Quiz")

        self.load_recent_files()

        if (
            self.parent
            and hasattr(self.parent, "ui")
            and hasattr(self.parent.ui, "file_input")
        ):
            self.file_combobox = self.parent.ui.file_input
            self.file_combobox.setEditable(False)
            self.setup_combobox()
            self.file_combobox.currentIndexChanged.connect(self.on_file_selected)

        if (
            self.parent
            and hasattr(self.parent, "ui")
            and hasattr(self.parent.ui, "browse_file_btn")
        ):
            self.browse_btn = self.parent.ui.browse_file_btn
            self.browse_btn.clicked.connect(self.browse_file)

    def setup_combobox(self):
        self.file_combobox.clear()

        self.file_combobox.addItem("-- Select a file --", None)

        if self.recent_files:
            for file_path in self.recent_files:
                file_name = os.path.basename(file_path)
                self.file_combobox.addItem(file_name, file_path)

        self.file_combobox.setCurrentIndex(0)

    def on_file_selected(self, index):
        if index == 0:
            return

        file_path = self.file_combobox.itemData(index)

        if file_path and os.path.exists(file_path):
            self.load_quiz_file(file_path)
        else:
            self.remove_from_recent(file_path)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Select Quiz File",
            "",
            "Quiz Files (*.json *.txt *.csv);;All Files (*.*)",
        )

        if file_path:
            self.add_to_recent(file_path)
            self.load_quiz_file(file_path)
            self.setup_combobox()
            for i in range(self.file_combobox.count()):
                if self.file_combobox.itemData(i) == file_path:
                    self.file_combobox.setCurrentIndex(i)
                    break

    def load_quiz_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error loading file: {e}")

    def add_to_recent(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)

        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[: self.max_recent_files]
        self.save_recent_files()

    def remove_from_recent(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
            self.save_recent_files()
            self.setup_combobox()

    def load_recent_files(self):
        self.recent_files = self.settings.value("recent_files", [], type=list)
        self.recent_files = [f for f in self.recent_files if os.path.exists(f)]

    def save_recent_files(self):
        self.settings.setValue("recent_files", self.recent_files)
