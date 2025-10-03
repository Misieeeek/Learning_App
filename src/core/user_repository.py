from core.database_manager import Database_Manager
from core.password_hasher import Password_Hasher


class User_Repository:
    def __init__(self, db_path="student.db"):
        self.db_path = db_path
        self.db_manager = Database_Manager()

    def save_user(self, username, password):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        hashed_pass = Password_Hasher.hash(password)

        self.create_user_table()

        if self.check_username_exists(username):
            print("Username is used")
            connection.close()
            return
        cursor.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, hashed_pass),
        )

        connection.commit()
        connection.close()

    def create_user_table(self):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        query_create_tbl_user = """CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)"""
        cursor.execute(query_create_tbl_user)

        connection.commit()
        connection.close()

    def check_username_exists(self, username):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        cursor.execute("SELECT COUNT(*) FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        connection.close()

        return result[0] > 0

    def get_user_password(self, username):
        connection, cursor = self.db_manager.get_connection_and_cursor()

        cursor.execute("SELECT password FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()

        connection.close()
        return result

    def verify_user(self, username, password):
        result = self.get_user_password(username)
        if result is None:
            return False

        hashed_password = result[0]
        return Password_Hasher.verify(password, hashed_password)
