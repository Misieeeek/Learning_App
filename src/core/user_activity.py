import calendar
from datetime import datetime, timedelta

from core.database_manager import Database_Manager


class User_Activity:
    def __init__(self, db_path="student.db"):
        self.db_path = db_path
        self.db_manager = Database_Manager()

    def save_activity(self, username, start_time, end_time):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        self.create_activity_table()

        user_id = self.db_manager.get_user_id(username)
        if user_id is None:
            return

        cursor.execute(
            "INSERT INTO activity (user_id, start_time, end_time) VALUES (?, ?, ?)",
            (user_id, start_time, end_time),
        )

        connection.commit()
        connection.close()

    def create_activity_table(self):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        query_create_tbl_activity = """CREATE TABLE IF NOT EXISTS activity(activity_id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES user(user_id), start_time TEXT, end_time TEXT)"""
        cursor.execute(query_create_tbl_activity)

        connection.commit()
        connection.close()

    def get_user_day_activity(self, user_id, date):
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                date = datetime.strptime(date, "%Y-%m-%d")

        start_of_day = date.replace(hour=0, minute=0, second=0)
        end_of_day = start_of_day + timedelta(days=1)

        start_str = start_of_day.strftime("%Y-%m-%d %H:%M:%S")
        end_str = end_of_day.strftime("%Y-%m-%d %H:%M:%S")

        connection, cursor = self.db_manager.get_connection_and_cursor()
        cursor.execute(
            "SELECT start_time, end_time FROM activity WHERE user_id = ? AND start_time >= ? AND start_time < ? ORDER BY start_time ASC",
            (user_id, start_str, end_str),
        )
        result = cursor.fetchall()
        connection.close()
        return result

    def get_user_week_activity(self, user_id, input_date):
        if isinstance(input_date, str):
            input_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")

        weekday = input_date.weekday()
        start_of_week = input_date - timedelta(days=weekday)
        week_table = []
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d %H:%M:%S")
            day_result = self.get_user_day_activity(user_id, date_str)
            if day_result:
                week_table.append(day_result)
            else:
                week_table.append(0.0)

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
                year_table.append(day_result)
            else:
                year_table.append(0.0)
        return year_table
