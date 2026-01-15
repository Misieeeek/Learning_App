import csv
from typing import Any, Dict, List


class csv_parser:
    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        questions = []

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            fieldnames = reader.fieldnames
            if fieldnames is None:
                raise ValueError("CSV file has no headers")

            if "Question" not in fieldnames:
                raise ValueError("CSV file missing 'Question' column")
            if "CorrectIndex" not in fieldnames:
                raise ValueError("CSV file missing 'CorrectIndex' column")

            for row_num, row in enumerate(reader, start=2):  # 1 = header
                question_text = row.get("Question", "").strip()

                if not question_text:
                    raise ValueError(f"Row {row_num}: Empty question")

                answers = []
                for i in range(1, 10):
                    answer_key = f"Answer{i}"
                    if answer_key in row:
                        answer = row[answer_key].strip()
                        if answer:
                            answers.append(answer)

                if len(answers) < 2:
                    raise ValueError(
                        f"Row {row_num}: Question must have at least 2 answers"
                    )

                try:
                    correct_index = int(row["CorrectIndex"])
                except ValueError:
                    raise ValueError(f"Row {row_num}: CorrectIndex must be a number")

                if correct_index < 0 or correct_index >= len(answers):
                    raise ValueError(
                        f"Row {row_num}: CorrectIndex {correct_index} out of range "
                        f"(must be 0-{len(answers) - 1})"
                    )

                questions.append(
                    {
                        "question": question_text,
                        "answers": answers,
                        "correct": correct_index,
                    }
                )

        if not questions:
            raise ValueError("No questions found in CSV file")

        return questions
