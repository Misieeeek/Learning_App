import sqlite3

from core.user_activity import User_Activity
from core.user_repository import User_Repository

# from core.todo_repo import Todo


class Database_Manager:
    def __init__(self, db_path: str = "student.db"):
        self.db_path = db_path
        self.activity_controller = User_Activity(self.db_path)
        self.user_repo = User_Repository(self.db_path)
        # self.todo_repo = Todo()

    def get_connection_and_cursor(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        return connection, cursor

    def create_tables(self):
        self.user_repo.create_user_table()
        self.activity_controller.create_activity_table()
        # self.todo_repo.create_todo_table()

    def get_user_id(self, username):
        connection, cursor = self.get_connection_and_cursor()
        cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else None

