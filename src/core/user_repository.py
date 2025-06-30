import sqlite3

from core.password_hasher import Password_Hasher


class User_Repository:
    def save_user(self, username, password):
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        hashed_pass = Password_Hasher.hash(self, password)

        self.create_user_table()

        if self.check_username_exists(username):
            print("Username is used")
            connection.close()
            return

        cursor.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, hashed_pass),
        )

        print("User added")
        connection.commit()
        connection.close()

    def create_user_table(self):
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        query_create_tbl_user = """CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)"""
        cursor.execute(query_create_tbl_user)

        print("User table created")
        connection.commit()
        connection.close()

    def check_username_exists(self, username):
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        connection.close()

        return result[0] > 0

    def get_user_password(self, username):
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("SELECT password FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()

        connection.close()
        return result
