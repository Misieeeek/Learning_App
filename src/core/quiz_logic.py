import random
from typing import Any, Dict, Optional

from core.parsers.csv_parser import csv_parser
from core.parsers.json_parser import JSON_parser
from core.parsers.txt_parser import txt_parser


class Quiz_Logic:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.total_answered = 0
        self.user_answers = []

        self.randomize_questions = False
        self.randomize_answers = False
        self.show_score_after_each = False
        self.show_answers = True

        self.json_parser = JSON_parser()
        self.csv_parser = csv_parser()
        self.txt_parser = txt_parser()

        self._load_questions()

    def _load_questions(self):
        file_ext = self.file_path.lower().split(".")[-1]

        if file_ext == "json":
            self.questions = self.json_parser.parse(self.file_path)
        elif file_ext == "txt":
            self.questions = self.txt_parser.parse(self.file_path)
        elif file_ext == "csv":
            self.questions = self.csv_parser.parse(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def configure(self, params: Dict[str, Any]):
        self.randomize_questions = params.get("randomize_questions", False)
        self.randomize_answers = params.get("randomize_answers", False)
        self.show_score_after_each = params.get("show_score_after_each", False)
        self.show_answers = params.get("show_answers", True)

        self.current_question_index = 0
        self.score = 0
        self.total_answered = 0
        self.user_answers = []

        if self.randomize_questions:
            random.shuffle(self.questions)

    def get_total_questions(self) -> int:
        return len(self.questions)

    def get_next_question(self) -> Optional[Dict[str, Any]]:
        if self.current_question_index >= len(self.questions):
            return None

        question = self.questions[self.current_question_index].copy()

        if self.randomize_answers:
            correct_answer = question["answers"][question["correct"]]
            random.shuffle(question["answers"])
            question["correct"] = question["answers"].index(correct_answer)

        return question

    def submit_answer(self, answer_index: int) -> Dict[str, Any]:
        if self.current_question_index >= len(self.questions):
            return {"error": "No more questions"}

        question = self.questions[self.current_question_index]
        is_correct = answer_index == question["correct"]

        if is_correct:
            self.score += 1

        self.total_answered += 1
        self.user_answers.append(
            {
                "question_index": self.current_question_index,
                "user_answer": answer_index,
                "correct_answer": question["correct"],
                "is_correct": is_correct,
            }
        )

        self.current_question_index += 1

        result = {
            "is_correct": is_correct,
            "correct_answer_index": question["correct"],
        }

        if self.show_score_after_each:
            result["current_score"] = self.score
            result["total_answered"] = self.total_answered

        return result

    def get_results(self) -> Dict[str, Any]:
        total = len(self.questions)
        percentage = (self.score / total * 100) if total > 0 else 0

        return {
            "score": self.score,
            "total": total,
            "percentage": percentage,
            "answers": self.user_answers if self.show_answers else [],
        }

    def reset(self):
        self.current_question_index = 0
        self.score = 0
        self.total_answered = 0
        self.user_answers = []
