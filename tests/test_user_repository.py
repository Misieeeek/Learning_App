import os
import sqlite3
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from core.register import User_Repository


class Test_User_Repository(unittest.TestCase):
    def setUp(self):
        self.db_path = "student.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.ur = User_Repository(self.db_path)
        self.ur.create_user_table()
        self.username = "testuser"
        self.password = "testpassword"
        self.ur.save_user(self.username, self.password)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_user_table_table_exists(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user'"
        )
        table = cursor.fetchone()
        self.assertIsNotNone(table)
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        expected_columns = ["user_id", "username", "password"]
        self.assertEqual(column_names, expected_columns)
        connection.close()

    def test_log_in_success(self):
        result = self.ur.verify_user(self.username, self.password)
        self.assertTrue(result)

    def test_log_in_fail_password(self):
        result = self.ur.verify_user(self.username, "wrongpassword")
        self.assertFalse(result)

    def test_log_in_fail_username(self):
        result = self.ur.verify_user("wronguser", self.password)
        self.assertFalse(result)

    def test_log_in_fail_both(self):
        result = self.ur.verify_user("wronguser", "wrongpassword")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
