import os

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

from core.quiz_logic import Quiz_Logic


class Quiz_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.max_recent_files = 5
        self.settings = QSettings("LearningApp", "Quiz")

        self.quiz_logic = None
        self.current_file_path = None

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

        if (
            self.parent
            and hasattr(self.parent, "ui")
            and hasattr(self.parent.ui, "start_quiz_btn")
        ):
            self.start_quiz_btn = self.parent.ui.start_quiz_btn
            self.start_quiz_btn.clicked.connect(self.start_quiz)
            self.start_quiz_btn.setEnabled(False)

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
            self.current_file_path = None
            self.start_quiz_btn.setEnabled(False)
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
            self.quiz_logic = Quiz_Logic(file_path)
            self.current_file_path = file_path
            self.start_quiz_btn.setEnabled(True)
        except Exception as e:
            print(f"Error loading quiz file: {e}")
            QMessageBox.critical(
                self.parent,
                "Error Loading Quiz",
                f"Failed to load quiz file:\n{str(e)}",
            )
            self.quiz_logic = None
            self.current_file_path = None
            self.start_quiz_btn.setEnabled(False)

    def start_quiz(self):
        if not self.quiz_logic:
            QMessageBox.warning(
                self.parent, "No Quiz Loaded", "Please select a quiz file first."
            )
            return

        params = self.get_quiz_parameters()

        self.quiz_logic.configure(params)

        if hasattr(self.parent, "ui") and hasattr(
            self.parent.ui, "quiz_stacked_widget"
        ):
            self.parent.ui.quiz_stacked_widget.setCurrentWidget(
                self.parent.ui.question_widget
            )

        self.show_next_question()

    def get_quiz_parameters(self):
        params = {
            "randomize_questions": False,
            "randomize_answers": False,
            "show_score_after_each": False,
            "show_answers": False,
        }

        # Sprawdź radio buttony dla randomizacji pytań
        if hasattr(self.parent, "ui"):
            if (
                hasattr(self.parent.ui, "rqoy_rbtn")
                and self.parent.ui.rqoy_rbtn.isChecked()
            ):
                params["randomize_questions"] = True

            # Randomizacja odpowiedzi
            if (
                hasattr(self.parent.ui, "raoy_rbtn")
                and self.parent.ui.raoy_rbtn.isChecked()
            ):
                params["randomize_answers"] = True

            # Pokaż wynik po każdym pytaniu
            if (
                hasattr(self.parent.ui, "aeq_rbtn")
                and self.parent.ui.aeq_rbtn.isChecked()
            ):
                params["show_score_after_each"] = True

            # Pokaż odpowiedzi
            if (
                hasattr(self.parent.ui, "say_rbtn")
                and self.parent.ui.say_rbtn.isChecked()
            ):
                params["show_answers"] = True

        return params

    def show_next_question(self):
        """Pokaż następne pytanie używając QuizLogic"""
        if not self.quiz_logic:
            return

        question_data = self.quiz_logic.get_next_question()

        if question_data is None:
            # Quiz zakończony
            self.show_results()
            return

        # Wyświetl pytanie w UI
        # TODO: Zaktualizuj widgety pytania z question_data
        print(f"Question: {question_data['question']}")
        print(f"Answers: {question_data['answers']}")

    def show_results(self):
        """Pokaż wyniki quizu"""
        if not self.quiz_logic:
            return

        results = self.quiz_logic.get_results()

        QMessageBox.information(
            self.parent,
            "Quiz Completed!",
            f"Score: {results['score']}/{results['total']}\n"
            f"Percentage: {results['percentage']:.1f}%",
        )

        # Wróć do ekranu parametrów
        if hasattr(self.parent, "ui") and hasattr(
            self.parent.ui, "quiz_stacked_widget"
        ):
            self.parent.ui.quiz_stacked_widget.setCurrentWidget(
                self.parent.ui.params_widget
            )

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
