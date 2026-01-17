import os

from PySide6.QtCore import QSettings, Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from core.quiz_logic import Quiz_Logic


class ClickableLabel(QLabel):
    def __init__(self, text, callback, index):
        super().__init__(text)
        self.callback = callback
        self.index = index
        self.is_enabled = True

    def mousePressEvent(self, event):
        if self.is_enabled:
            self.callback(self.index)

    def setEnabled(self, enabled):
        self.is_enabled = enabled


class Quiz_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.max_recent_files = 5
        self.settings = QSettings("LearningApp", "Quiz")

        self.quiz_logic = None
        self.current_file_path = None

        self.answer_buttons = []
        self.answers_layout = None
        self.answers_container = None

        self.progress_indicators = []
        self.progress_layout = None
        self.progress_container = None

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

        if (
            self.parent
            and hasattr(self.parent, "ui")
            and hasattr(self.parent.ui, "stop_btn")
        ):
            self.stop_btn = self.parent.ui.stop_btn
            self.stop_btn.clicked.connect(self.stop_quiz)

        if (
            self.parent
            and hasattr(self.parent, "ui")
            and hasattr(self.parent.ui, "next_quiz_question_btn")
        ):
            self.next_btn = self.parent.ui.next_quiz_question_btn
            self.next_btn.clicked.connect(self.next_question)

        if (
            self.parent
            and hasattr(self.parent, "ui")
            and hasattr(self.parent.ui, "prev_quiz_question_btn")
        ):
            self.prev_btn = self.parent.ui.prev_quiz_question_btn
            self.prev_btn.clicked.connect(self.previous_question)

        self.setup_answer_area()

        self.setup_progress_indicators()

    def setup_answer_area(self):
        if not self.parent or not hasattr(self.parent, "ui"):
            return

        if not hasattr(self.parent.ui, "question_widget"):
            return

        self.answers_layout = QVBoxLayout()
        self.answers_layout.setSpacing(10)
        self.answers_layout.setContentsMargins(0, 0, 0, 0)

        self.answers_container = QWidget(self.parent.ui.question_widget)
        self.answers_container.setGeometry(40, 150, 700, 280)
        self.answers_container.setLayout(self.answers_layout)

    def setup_progress_indicators(self):
        if not self.parent or not hasattr(self.parent, "ui"):
            return

        if not hasattr(self.parent.ui, "question_widget"):
            return

        self.progress_layout = QHBoxLayout()
        self.progress_layout.setSpacing(6)
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_layout.setAlignment(Qt.AlignCenter)

        self.progress_container = QWidget(self.parent.ui.question_widget)
        self.progress_container.setGeometry(325, 465, 200, 30)
        self.progress_container.setLayout(self.progress_layout)

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

        self.update_progress_indicators()

        if hasattr(self.parent, "ui") and hasattr(
            self.parent.ui, "quiz_stacked_widget"
        ):
            self.parent.ui.quiz_stacked_widget.setCurrentWidget(
                self.parent.ui.question_widget
            )

        self.show_current_question()

    def get_quiz_parameters(self):
        params = {
            "randomize_questions": False,
            "randomize_answers": False,
            "show_score_after_each": False,
            "show_answers": False,
        }

        if hasattr(self.parent, "ui"):
            if (
                hasattr(self.parent.ui, "rqoy_rbtn")
                and self.parent.ui.rqoy_rbtn.isChecked()
            ):
                params["randomize_questions"] = True

            if (
                hasattr(self.parent.ui, "raoy_rbtn")
                and self.parent.ui.raoy_rbtn.isChecked()
            ):
                params["randomize_answers"] = True

            if (
                hasattr(self.parent.ui, "aeq_rbtn")
                and self.parent.ui.aeq_rbtn.isChecked()
            ):
                params["show_score_after_each"] = True

            if (
                hasattr(self.parent.ui, "say_rbtn")
                and self.parent.ui.say_rbtn.isChecked()
            ):
                params["show_answers"] = True

        return params

    def update_navigation_buttons(self):
        if not self.quiz_logic:
            return

        current = self.quiz_logic.current_question_index
        total = self.quiz_logic.get_total_questions()

        if hasattr(self, "prev_btn"):
            self.prev_btn.setEnabled(current > 0)

        if hasattr(self, "next_btn"):
            self.next_btn.setEnabled(current < total - 1)

    def show_current_question(self):
        if not self.quiz_logic:
            return

        current_index = self.quiz_logic.current_question_index

        if current_index >= self.quiz_logic.get_total_questions():
            self.show_results()
            return

        question_data = self.quiz_logic.questions[current_index].copy()

        if hasattr(self.parent, "ui") and hasattr(self.parent.ui, "question_lbl"):
            self.parent.ui.question_lbl.setText(question_data["question"])
            self.parent.ui.question_lbl.setStyleSheet("color: white;")

        self.generate_answer_buttons(question_data["answers"])

        self.update_progress_indicators()

        self.update_navigation_buttons()

        self.restore_answer_state(current_index)

    def next_question(self):
        if not self.quiz_logic:
            return

        total = self.quiz_logic.get_total_questions()
        if self.quiz_logic.current_question_index < total - 1:
            self.quiz_logic.current_question_index += 1
            self.show_current_question()

    def previous_question(self):
        if not self.quiz_logic:
            return

        if self.quiz_logic.current_question_index > 0:
            self.quiz_logic.current_question_index -= 1
            self.show_current_question()

    def update_progress_indicators(self):
        if not self.quiz_logic or not self.progress_layout:
            return

        for indicator in self.progress_indicators:
            indicator.deleteLater()
        self.progress_indicators.clear()

        total_questions = self.quiz_logic.get_total_questions()
        current_index = self.quiz_logic.current_question_index

        visible_indices = self._get_visible_question_indices(
            current_index, total_questions
        )

        for i, q_index in enumerate(visible_indices):
            if q_index == -1:
                dots_label = QLabel("...")
                dots_label.setStyleSheet("color: white; font-size: 12px;")
                self.progress_layout.addWidget(dots_label)
                self.progress_indicators.append(dots_label)
            else:
                if q_index == current_index:
                    indicator = QLabel(str(q_index + 1))  # +1 bo numerujemy od 1
                    indicator.setFixedSize(20, 20)
                else:
                    indicator = QLabel("●")
                    indicator.setFixedSize(15, 15)

                indicator.setAlignment(Qt.AlignCenter)

                color = self._get_indicator_color(q_index)

                if q_index == current_index:
                    indicator.setStyleSheet(f"""
                        color: {color};
                        font-size: 14px;
                        font-weight: bold;
                    """)
                else:
                    indicator.setStyleSheet(f"""
                        color: {color};
                        font-size: 12px;
                    """)

                self.progress_layout.addWidget(indicator)
                self.progress_indicators.append(indicator)

    def generate_answer_buttons(self, answers):
        self.clear_answer_buttons()

        font = QFont()
        font.setFamilies(["FiraMono Nerd Font"])
        font.setPointSize(11)

        for index, answer in enumerate(answers):
            btn = ClickableLabel(answer, self.check_answer, index)
            btn.setFont(font)
            btn.setWordWrap(True)
            btn.setStyleSheet("""
                QLabel {
                    background-color: rgb(47, 47, 47); 
                    color: white;
                    padding: 10px;
                    border: 2px solid transparent;
                }
                QLabel:hover {
                    background-color: rgb(67, 67, 67);
                    border: 2px solid rgb(100, 100, 100);
                }
            """)
            btn.setMinimumHeight(50)
            btn.setCursor(Qt.PointingHandCursor)

            self.answers_layout.addWidget(btn)
            self.answer_buttons.append(btn)

    def clear_answer_buttons(self):
        for btn in self.answer_buttons:
            btn.deleteLater()
        self.answer_buttons.clear()

    def check_answer(self, answer_index):
        if not self.quiz_logic:
            return

        current_index = self.quiz_logic.current_question_index

        already_answered = any(
            ans["question_index"] == current_index
            for ans in self.quiz_logic.user_answers
        )

        if already_answered:
            old_answer = next(
                (
                    ans
                    for ans in self.quiz_logic.user_answers
                    if ans["question_index"] == current_index
                ),
                None,
            )
            if old_answer and old_answer["is_correct"]:
                self.quiz_logic.score -= 1
            self.quiz_logic.total_answered -= 1

            self.quiz_logic.user_answers = [
                ans
                for ans in self.quiz_logic.user_answers
                if ans["question_index"] != current_index
            ]

        question = self.quiz_logic.questions[current_index]
        is_correct = answer_index == question["correct"]

        if is_correct:
            self.quiz_logic.score += 1

        self.quiz_logic.total_answered += 1

        self.quiz_logic.user_answers.append(
            {
                "question_index": current_index,
                "user_answer": answer_index,
                "correct_answer": question["correct"],
                "is_correct": is_correct,
            }
        )

        correct_index = question["correct"]

        self.answer_buttons[correct_index].setStyleSheet("""
            QLabel {
                background-color: rgb(0, 150, 0);
                color: white;
                padding: 10px;
                border: 2px solid rgb(0, 200, 0);
            }
        """)

        if not is_correct:
            self.answer_buttons[answer_index].setStyleSheet("""
                QLabel {
                    background-color: rgb(150, 0, 0);
                    color: white;
                    padding: 10px;
                    border: 2px solid rgb(200, 0, 0);
                }
            """)

        for btn in self.answer_buttons:
            btn.setEnabled(False)

        self.update_progress_indicators()

        if self.quiz_logic.show_score_after_each:
            if hasattr(self.parent, "ui") and hasattr(self.parent.ui, "question_lbl"):
                score_text = f"\n\nWynik: {self.quiz_logic.score}/{self.quiz_logic.total_answered}"
                current_text = self.parent.ui.question_lbl.text()
                if "\n\nWynik:" in current_text:
                    current_text = current_text.split("\n\nWynik:")[0]
                self.parent.ui.question_lbl.setText(current_text + score_text)

        if self.quiz_logic.show_answers:
            if current_index < self.quiz_logic.get_total_questions() - 1:
                QTimer.singleShot(1500, self.next_question)
            else:
                QTimer.singleShot(1500, self.show_results)

    def restore_answer_state(self, question_index):
        if not self.quiz_logic:
            return

        user_answer = next(
            (
                ans
                for ans in self.quiz_logic.user_answers
                if ans["question_index"] == question_index
            ),
            None,
        )

        if user_answer:
            correct_index = user_answer["correct_answer"]
            user_index = user_answer["user_answer"]

            if correct_index < len(self.answer_buttons):
                self.answer_buttons[correct_index].setStyleSheet("""
                    QLabel {
                        background-color: rgb(0, 150, 0);
                        color: white;
                        padding: 10px;
                        border: 2px solid rgb(0, 200, 0);
                    }
                """)

            if not user_answer["is_correct"] and user_index < len(self.answer_buttons):
                self.answer_buttons[user_index].setStyleSheet("""
                    QLabel {
                        background-color: rgb(150, 0, 0);
                        color: white;
                        padding: 10px;
                        border: 2px solid rgb(200, 0, 0);
                    }
                """)

            for btn in self.answer_buttons:
                btn.setEnabled(False)

    def update_progress_indicators(self):
        if not self.quiz_logic or not self.progress_layout:
            return

        for indicator in self.progress_indicators:
            indicator.deleteLater()
        self.progress_indicators.clear()

        total_questions = self.quiz_logic.get_total_questions()
        current_index = self.quiz_logic.current_question_index

        visible_indices = self._get_visible_question_indices(
            current_index, total_questions
        )

        for i, q_index in enumerate(visible_indices):
            if q_index == -1:
                dots_label = QLabel("...")
                dots_label.setStyleSheet("color: white; font-size: 12px;")
                self.progress_layout.addWidget(dots_label)
                self.progress_indicators.append(dots_label)
            else:
                if q_index == current_index:
                    indicator = QLabel(str(q_index + 1))
                    indicator.setFixedSize(20, 20)
                else:
                    indicator = QLabel("●")
                    indicator.setFixedSize(15, 15)

                indicator.setAlignment(Qt.AlignCenter)

                color = self._get_indicator_color(q_index)

                if q_index == current_index:
                    indicator.setStyleSheet(f"""
                        color: {color};
                        font-size: 14px;
                        font-weight: bold;
                    """)
                else:
                    indicator.setStyleSheet(f"""
                        color: {color};
                        font-size: 12px;
                    """)

                self.progress_layout.addWidget(indicator)
                self.progress_indicators.append(indicator)

    def _get_visible_question_indices(self, current, total):
        if total <= 7:
            return list(range(total))

        visible = []

        if current < 4:
            visible = list(range(5))
            visible.append(-1)
            visible.append(total - 1)

        elif current >= total - 4:
            visible.append(0)
            visible.append(-1)
            visible.extend(list(range(total - 5, total)))

        else:
            visible.append(0)
            visible.append(-1)
            visible.extend([current - 1, current, current + 1])
            visible.append(-1)
            visible.append(total - 1)

        return visible

    def _get_indicator_color(self, question_index):
        if not self.quiz_logic:
            return "gray"

        user_answer = next(
            (
                ans
                for ans in self.quiz_logic.user_answers
                if ans["question_index"] == question_index
            ),
            None,
        )

        if user_answer is None:
            return "gray"
        elif user_answer["is_correct"]:
            return "rgb(0, 200, 0)"
        else:
            return "rgb(200, 0, 0)"

    def show_results(self):
        if not self.quiz_logic:
            return

        results = self.quiz_logic.get_results()

        QMessageBox.information(
            self.parent,
            "Quiz Completed!",
            f"Score: {results['score']}/{results['total']}\n"
            f"Percentage: {results['percentage']:.1f}%",
        )

        self.stop_quiz()

    def stop_quiz(self):
        if self.quiz_logic:
            self.quiz_logic.reset()

        self.clear_answer_buttons()

        for indicator in self.progress_indicators:
            indicator.deleteLater()
        self.progress_indicators.clear()

        if hasattr(self.parent, "ui") and hasattr(self.parent.ui, "question_lbl"):
            self.parent.ui.question_lbl.setText("")

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
