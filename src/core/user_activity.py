import calendar
import sqlite3
from datetime import datetime, timedelta


class User_Activity:
    def __init__(self, db_path="student.db"):
        self.db_path = db_path

    def get_connection_and_cursor(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        return connection, cursor

    def save_activity(self, username, datetime):
        connection, cursor = self.get_connection_and_cursor()

        self.create_activity_table()

        user_id = self.get_user_id(username)
        if user_id is None:
            return

        cursor.execute(
            "INSERT INTO activity (user_id, datetime) VALUES (?, ?)",
            (user_id, datetime),
        )

        connection.commit()
        connection.close()

    def get_user_id(self, username):
        connection, cursor = self.get_connection_and_cursor()
        cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else None

    def create_activity_table(self):
        connection, cursor = self.get_connection_and_cursor()

        query_create_tbl_activity = """CREATE TABLE IF NOT EXISTS activity(activity_id INTEGER PRIMARY KEY, user_id INTEGER, datetime TEXT, FOREIGN KEY (user_id) REFERENCES user(user_id))"""
        cursor.execute(query_create_tbl_activity)

        connection.commit()
        connection.close()

    def get_user_day_activity(self, user_id, date):
        connection, cursor = self.get_connection_and_cursor()

        cursor.execute(
            "SELECT datetime FROM activity WHERE user_id = ? AND datetime LIKE ?",
            (user_id, date + "%"),
        )
        result = cursor.fetchone()

        connection.close()
        return result

    def get_user_week_activity(self, user_id, input_date):
        weekday = input_date.weekday()
        start_of_week = input_date - timedelta(days=weekday)
        week_table = []
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d %H:%M:%S")
            day_result = self.get_user_day_activity(user_id, date_str)
            if day_result:
                week_table.append(day_result[0])

        return week_table

    def get_user_year_activity(self, user_id):
        current_year = datetime.now().year
        num_days = 366 if calendar.isleap(current_year) else 365
        year_table = []
        start_date = datetime(current_year, 1, 1)
        for i in range(num_days):
            day = start_date + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d %H:%M:%S")
            day_result = self.get_user_day_activity(user_id, date_str)
            if day_result:
                year_table.append(day_result[0])
        return year_table
