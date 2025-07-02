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
        self.ur.get_connection_and_cursor = lambda: (
            sqlite3.connect(self.db_path),
            sqlite3.connect(self.db_path).cursor(),
        )
        self.ur.create_user_table()
        self.username = "testuser"
        self.password = "testpassword"
        self.ur.save_user(self.username, self.password)

    def test_create_user_table_table_exists(self):
        self.setUp()
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
        self.setUp()
        result = self.ur.verify_user("testuser", "testpassword")
        self.assertTrue(result)

    def test_log_in_fail_password(self):
        self.setUp()
        result = self.ur.verify_user("testuser", "wrongpassword")
        self.assertFalse(result)

    def test_log_in_fail_username(self):
        self.setUp()
        result = self.ur.verify_user("wronguser", "testpassword")
        self.assertFalse(result)

    def test_log_in_fail_both(self):
        self.setUp()
        result = self.ur.verify_user("wronguser", "wrongpassword")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
