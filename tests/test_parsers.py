import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from core.parsers.csv_parser import csv_parser
from core.parsers.json_parser import JSON_parser
from core.parsers.txt_parser import txt_parser


class TestJSONParser(unittest.TestCase):
    def setUp(self):
        self.parser = JSON_parser()
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")

    def test_valid_json_from_file(self):
        file_path = os.path.join(self.test_data_dir, "example_quiz.json")

        if not os.path.exists(file_path):
            self.skipTest(f"Test file not found: {file_path}")

        questions = self.parser.parse(file_path)

        self.assertGreater(len(questions), 0, "Should have at least one question")

        first_q = questions[0]
        self.assertIn("question", first_q)
        self.assertIn("answers", first_q)
        self.assertIn("correct", first_q)

        self.assertIsInstance(first_q["question"], str)
        self.assertIsInstance(first_q["answers"], list)
        self.assertIsInstance(first_q["correct"], int)

        self.assertGreaterEqual(first_q["correct"], 0)
        self.assertLess(first_q["correct"], len(first_q["answers"]))

    def test_all_json_questions_valid(self):
        file_path = os.path.join(self.test_data_dir, "example_quiz.json")

        if not os.path.exists(file_path):
            self.skipTest(f"Test file not found: {file_path}")

        questions = self.parser.parse(file_path)

        for i, q in enumerate(questions):
            with self.subTest(question=i):
                self.assertTrue(q["question"].strip(), f"Question {i} is empty")

                self.assertGreaterEqual(
                    len(q["answers"]), 2, f"Question {i} has less than 2 answers"
                )

                self.assertGreaterEqual(
                    q["correct"], 0, f"Question {i} has negative correct index"
                )
                self.assertLess(
                    q["correct"],
                    len(q["answers"]),
                    f"Question {i} has correct index out of range",
                )


class TestTXTParser(unittest.TestCase):
    def setUp(self):
        self.parser = txt_parser()
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")

    def test_valid_txt_from_file(self):
        file_path = os.path.join(self.test_data_dir, "example_quiz.txt")

        if not os.path.exists(file_path):
            self.skipTest(f"Test file not found: {file_path}")

        questions = self.parser.parse(file_path)

        self.assertGreater(len(questions), 0, "Should have at least one question")

        first_q = questions[0]
        self.assertIn("question", first_q)
        self.assertIn("answers", first_q)
        self.assertIn("correct", first_q)

        for i, q in enumerate(questions):
            with self.subTest(question=i):
                self.assertGreaterEqual(
                    q["correct"], 0, f"Question {i}: No correct answer marked"
                )

    def test_txt_format_with_equals_one(self):
        file_path = os.path.join(self.test_data_dir, "example_quiz.txt")

        if not os.path.exists(file_path):
            self.skipTest(f"Test file not found: {file_path}")

        questions = self.parser.parse(file_path)

        for i, q in enumerate(questions):
            for j, answer in enumerate(q["answers"]):
                with self.subTest(question=i, answer=j):
                    self.assertNotIn(
                        "=1", answer, f"Question {i}, Answer {j}: =1 marker not removed"
                    )

    def test_all_txt_questions_valid(self):
        file_path = os.path.join(self.test_data_dir, "example_quiz.txt")

        if not os.path.exists(file_path):
            self.skipTest(f"Test file not found: {file_path}")

        questions = self.parser.parse(file_path)

        for i, q in enumerate(questions):
            with self.subTest(question=i):
                self.assertTrue(q["question"].strip(), f"Question {i} is empty")

                self.assertGreaterEqual(
                    len(q["answers"]), 2, f"Question {i} has less than 2 answers"
                )

                self.assertGreaterEqual(
                    q["correct"], 0, f"Question {i} has negative correct index"
                )
                self.assertLess(
                    q["correct"],
                    len(q["answers"]),
                    f"Question {i} has correct index out of range",
                )


class TestCSVParser(unittest.TestCase):
    def setUp(self):
        self.parser = csv_parser()
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")

    def test_valid_csv_from_file(self):
        file_path = os.path.join(self.test_data_dir, "example_quiz.csv")

        if not os.path.exists(file_path):
            self.skipTest(f"Test file not found: {file_path}")

        questions = self.parser.parse(file_path)

        self.assertGreater(len(questions), 0, "Should have at least one question")

        first_q = questions[0]
        self.assertIn("question", first_q)
        self.assertIn("answers", first_q)
        self.assertIn("correct", first_q)

        self.assertIsInstance(first_q["question"], str)
        self.assertIsInstance(first_q["answers"], list)
        self.assertIsInstance(first_q["correct"], int)

    def test_all_csv_questions_valid(self):
        file_path = os.path.join(self.test_data_dir, "example_quiz.csv")

        if not os.path.exists(file_path):
            self.skipTest(f"Test file not found: {file_path}")

        questions = self.parser.parse(file_path)

        for i, q in enumerate(questions):
            with self.subTest(question=i):
                self.assertTrue(q["question"].strip(), f"Question {i} is empty")

                self.assertGreaterEqual(
                    len(q["answers"]), 2, f"Question {i} has less than 2 answers"
                )

                self.assertGreaterEqual(
                    q["correct"], 0, f"Question {i} has negative correct index"
                )
                self.assertLess(
                    q["correct"],
                    len(q["answers"]),
                    f"Question {i} has correct index out of range",
                )


class TestAllParsersConsistency(unittest.TestCase):
    def setUp(self):
        self.json_parser = JSON_parser()
        self.txt_parser = txt_parser()
        self.csv_parser = csv_parser()
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")

    def test_all_parsers_return_same_count(self):
        json_path = os.path.join(self.test_data_dir, "example_quiz.json")
        txt_path = os.path.join(self.test_data_dir, "example_quiz.txt")
        csv_path = os.path.join(self.test_data_dir, "example_quiz.csv")

        if not all(os.path.exists(p) for p in [json_path, txt_path, csv_path]):
            self.skipTest("Not all test files exist")

        json_questions = self.json_parser.parse(json_path)
        txt_questions = self.txt_parser.parse(txt_path)
        csv_questions = self.csv_parser.parse(csv_path)

        self.assertEqual(
            len(json_questions),
            len(txt_questions),
            "JSON and TXT should have same number of questions",
        )
        self.assertEqual(
            len(json_questions),
            len(csv_questions),
            "JSON and CSV should have same number of questions",
        )

    def test_all_parsers_return_same_questions(self):
        json_path = os.path.join(self.test_data_dir, "example_quiz.json")
        txt_path = os.path.join(self.test_data_dir, "example_quiz.txt")
        csv_path = os.path.join(self.test_data_dir, "example_quiz.csv")

        if not all(os.path.exists(p) for p in [json_path, txt_path, csv_path]):
            self.skipTest("Not all test files exist")

        json_questions = self.json_parser.parse(json_path)
        txt_questions = self.txt_parser.parse(txt_path)
        csv_questions = self.csv_parser.parse(csv_path)

        for i in range(len(json_questions)):
            with self.subTest(question=i):
                json_q = json_questions[i]["question"]
                txt_q = txt_questions[i]["question"]
                csv_q = csv_questions[i]["question"]

                self.assertEqual(
                    json_q, txt_q, f"Question {i}: JSON and TXT texts don't match"
                )
                self.assertEqual(
                    json_q, csv_q, f"Question {i}: JSON and CSV texts don't match"
                )

    def test_all_parsers_return_same_correct_answers(self):
        json_path = os.path.join(self.test_data_dir, "example_quiz.json")
        txt_path = os.path.join(self.test_data_dir, "example_quiz.txt")
        csv_path = os.path.join(self.test_data_dir, "example_quiz.csv")

        if not all(os.path.exists(p) for p in [json_path, txt_path, csv_path]):
            self.skipTest("Not all test files exist")

        json_questions = self.json_parser.parse(json_path)
        txt_questions = self.txt_parser.parse(txt_path)
        csv_questions = self.csv_parser.parse(csv_path)

        for i in range(len(json_questions)):
            with self.subTest(question=i):
                json_correct = json_questions[i]["correct"]
                txt_correct = txt_questions[i]["correct"]
                csv_correct = csv_questions[i]["correct"]

                self.assertEqual(
                    json_correct,
                    txt_correct,
                    f"Question {i}: JSON and TXT correct indices don't match",
                )
                self.assertEqual(
                    json_correct,
                    csv_correct,
                    f"Question {i}: JSON and CSV correct indices don't match",
                )


if __name__ == "__main__":
    import sys

    project_root = os.path.join(os.path.dirname(__file__), "..")
    sys.path.insert(0, project_root)

    unittest.main(verbosity=2)
