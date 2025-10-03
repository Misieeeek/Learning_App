from core.database_manager import Database_Manager


class Todo:
    def __init__(self, user_id, db_path="student.db"):
        self.db_path = db_path
        self.db_manager = Database_Manager()

    def create_todo_table(self):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        query_create_tbl_todo = """CREATE TABLE IF NOT EXISTS todo(todo_id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES user(user_id), item TEXT, personal_item_id INTEGER, priority INTEGER, date TEXT)"""
        cursor.execute(query_create_tbl_todo)

        connection.commit()
        connection.close()

    def add_todo_item(self, username, item, item_id, priority, date_added):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        user_id = self.db_manager.get_user_id(username)

        cursor.execute(
            "INSERT INTO todo (user_id, item, personal_item_id, priority, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, item, item_id, priority, date_added),
        )

        connection.commit()
        connection.close()

    def remove_todo_item(self, username, item_id):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        user_id = self.db_manager.get_user_id(username)

        cursor.execute(
            "DELETE FROM todo WHERE user_id = ? AND personal_item_id = ?",
            (user_id, item_id),
        )
        connection.commit()
        connection.close()

    def get_todo_items(self, username):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        user_id = self.db_manager.get_user_id(username)

        cursor.execute(
            "SELECT * FROM todo WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchall()
        connection.close()
        return result
