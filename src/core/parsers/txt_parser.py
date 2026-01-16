from typing import Any, Dict, List


class txt_parser:
    """
    Format TXT:
    Q: What is 2+2?
    A: 3
    A: 4=1
    A: 5
    A: 6

    Q: Capital of France?
    A: London
    A: Paris=1
    A: Berlin

    =1 means correct answer
    """

    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        questions = []
        current_question = None
        current_answers = []
        correct_index = -1

        for line_num, line in enumerate(lines, 1):
            if line.startswith("Q:"):
                if current_question is not None:
                    if correct_index == -1:
                        raise ValueError(
                            f"Question '{current_question}' has no correct answer marked with *"
                        )
                    questions.append(
                        {
                            "question": current_question,
                            "answers": current_answers,
                            "correct": correct_index,
                        }
                    )

                current_question = line[2:].strip()
                if not current_question:
                    raise ValueError(f"Line {line_num}: Empty question")
                current_answers = []
                correct_index = -1

            elif line.startswith("A:"):
                if current_question is None:
                    raise ValueError(f"Line {line_num}: Answer before question")

                answer = line[2:].strip()
                if answer.endswith("=1"):
                    if correct_index != -1:
                        raise ValueError(
                            f"Question '{current_question}' has multiple correct answers marked"
                        )
                    answer = answer[:-2].strip()
                    correct_index = len(current_answers)

                if not answer:
                    raise ValueError(f"Line {line_num}: Empty answer")

                current_answers.append(answer)

            else:
                raise ValueError(
                    f"Line {line_num}: Invalid format. Lines must start with 'Q:' or 'A:'"
                )

        if current_question is not None:
            if correct_index == -1:
                raise ValueError(
                    f"Question '{current_question}' has no correct answer marked with '=1'"
                )
            questions.append(
                {
                    "question": current_question,
                    "answers": current_answers,
                    "correct": correct_index,
                }
            )

        if not questions:
            raise ValueError("No questions found in file")

        return questions
