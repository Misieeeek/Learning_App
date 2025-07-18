import os
import sqlite3
import sys
import unittest
from datetime import datetime, timedelta

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from core.user_activity import User_Activity
from core.user_repository import User_Repository


class Test_User_Activity(unittest.TestCase):
    def setUp(self):
        self.db_path = "student.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.ur = User_Repository(self.db_path)
        self.ur.create_user_table()
        self.username = "testuser"
        self.password = "testpassword"
        self.ur.save_user(self.username, self.password)
        self.ua = User_Activity(self.db_path)
        self.datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ua.create_activity_table()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_activity_table_table_exists(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='activity'"
        )
        table = cursor.fetchone()
        self.assertIsNotNone(table)
        cursor.execute("PRAGMA table_info(activity)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        expected_columns = ["activity_id", "user_id", "datetime"]
        self.assertEqual(column_names, expected_columns)
        connection.close()

    def test_save_user(self):
        self.ua.save_activity(self.username, self.datetime_str)
        user_id = self.ua.get_user_id(self.username)
        today = datetime.now().strftime("%Y-%m-%d")
        result = self.ua.get_user_day_activity(user_id, today)
        self.assertEqual(result[0], self.datetime_str)

    def test_week_activity_correct(self):
        start_date = datetime.strptime("2025-07-11 16:57:58", "%Y-%m-%d %H:%M:%S")
        datetimes = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
            for i in range(17)
        ]
        correct_week = datetimes[10:17]

        for date in datetimes:
            self.ua.save_activity(self.username, date)

        user_id = self.ua.get_user_id(self.username)

        input_date = datetime.strptime("2025-07-25 16:57:58", "%Y-%m-%d %H:%M:%S")
        week = self.ua.get_user_week_activity(user_id, input_date)

        self.assertEqual(week, correct_week)

    def test_week_activity_missing_day(self):
        start_date = datetime.strptime("2025-07-11 16:57:58", "%Y-%m-%d %H:%M:%S")
        datetimes = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
            for i in range(17)
        ]

        missing_day = "2025-07-25 16:57:58"
        datetimes_with_gap = [dt for dt in datetimes if dt != missing_day]

        correct_week = [dt for dt in datetimes[10:17] if dt != missing_day]

        for date in datetimes_with_gap:
            self.ua.save_activity(self.username, date)

        user_id = self.ua.get_user_id(self.username)

        input_date = datetime.strptime("2025-07-25 16:57:58", "%Y-%m-%d %H:%M:%S")
        week = self.ua.get_user_week_activity(user_id, input_date)

        self.assertEqual(week, correct_week)
        self.assertNotIn(missing_day, week)


if __name__ == "__main__":
    unittest.main()
