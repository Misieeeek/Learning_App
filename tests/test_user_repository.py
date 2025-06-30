import os
import sqlite3
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from core.register import User_Repository


class Test_User_Repository(unittest.TestCase):
    def test_create_user_table_table_exists(self):
        ur = User_Repository()
        ur.create_user_table()

        connection = sqlite3.connect("student.db")
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


if __name__ == "__main__":
    unittest.main()
