import sqlite3

from password_hasher import Password_Hasher


class UserRepository:
    def save_user(self, username, password):
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        query_create_tbl_user = """CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)"""

        cursor.execute(query_create_tbl_user)

        hashed_pass = Password_Hasher.hash(self, password)

        cursor.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, hashed_pass),
        )
