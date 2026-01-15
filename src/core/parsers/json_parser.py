import json
from typing import Any, Dict, List


class JSON_parser:
    """
    Format JSON:
    {
        "questions": [
            {
                "question": "What is 2+2?",
                "answers": ["3", "4", "5", "6"],
                "correct": 1
            }
        ]
    }
    """

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            questions = data.get("questions", [])

        for i, q in enumerate(questions):
            if "question" not in q:
                raise ValueError(f"Question {i} missing 'question' field")
            if "answers" not in q or not isinstance(q["answers"], list):
                raise ValueError(f"Question {i} missing or invalid 'answers' field")
            if "correct" not in q or not isinstance(q["correct"], int):
                raise ValueError(f"Question {i} missing or invalid 'correct' field")
            if q["correct"] < 0 or q["correct"] >= len(q["answers"]):
                raise ValueError(f"Question {i} has invalid correct answer index")

        return questions
