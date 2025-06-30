import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from core.register import Register


class Test_Register(unittest.TestCase):
    def test_input_correct_normal(self):
        reg = Register("james", "123", "123")
        result = reg.input_correct()
        self.assertEqual(result, True)

    def test_input_correct_bad_c_password(self):
        reg = Register("james", "123", "12")
        result = reg.input_correct()
        self.assertEqual(result, False)

    def test_input_correct_empty_username(self):
        reg = Register("", "123", "123")
        result = reg.input_correct()
        self.assertEqual(result, False)

    def test_input_correct_empty_password(self):
        reg = Register("james", "", "12")
        result = reg.input_correct()
        self.assertEqual(result, False)

    def test_input_correct_empty_c_password(self):
        reg = Register("james", "123", "")
        result = reg.input_correct()
        self.assertEqual(result, False)

    def test_input_correct_empty_username_password(self):
        reg = Register("", "", "123")
        result = reg.input_correct()
        self.assertEqual(result, False)

    def test_input_correct_empty_username_c_password(self):
        reg = Register("", "123", "")
        result = reg.input_correct()
        self.assertEqual(result, False)

    def test_input_correct_empty_password_c_password(self):
        reg = Register("james", "", "")
        result = reg.input_correct()
        self.assertEqual(result, False)

    def test_input_correct_full_empty(self):
        reg = Register("", "", "")
        result = reg.input_correct()
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
