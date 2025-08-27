import os
import sqlite3
import sys
import unittest
from datetime import datetime

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from core.todo_repository import Todo
from core.user_repository import User_Repository


class Test_Todo(unittest.TestCase):
    def setUp(self):
        self.db_path = "student.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.todo = Todo(self.db_path)
        self.todo.create_todo_table()
        self.ur = User_Repository(self.db_path)
        self.ur.create_user_table()
        self.username = "testuser"
        self.password = "testpassword"
        self.ur.save_user(self.username, self.password)
        self.items = ["5 jumps", "89 squads", "Reading"]
        self.item_ids = [0, 1, 2]
        self.priorities = [5, 9, 522]
        self.todo_id = 1
        self.user_id = 1
        self.ur.save_user(self.username, self.password)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_todo_table_table_exists(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='todo'"
        )
        table = cursor.fetchone()
        self.assertIsNotNone(table)
        cursor.execute("PRAGMA table_info(todo)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        expected_columns = [
            "todo_id",
            "user_id",
            "item",
            "personal_item_id",
            "priority",
            "date",
        ]
        connection.close()
        self.assertEqual(column_names, expected_columns)

    def test_add_item(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.todo.add_todo_item(
            self.username, self.items[0], self.item_ids[0], self.priorities[0], date
        )
        result = self.todo.get_todo_items(self.username)
        connection.close()

        expected_result = (
            self.todo_id,
            self.user_id,
            self.items[0],
            self.item_ids[0],
            self.priorities[0],
            date,
        )
        self.assertEqual(result[0], expected_result)

    def test_remove(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        self.todo.remove_todo_item(self.username, self.item_ids[0])
        self.todo.remove_todo_item(self.username, self.item_ids[1])
        self.todo.remove_todo_item(self.username, self.item_ids[2])
        connection.close()
        result = self.todo.get_todo_items(self.username)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
