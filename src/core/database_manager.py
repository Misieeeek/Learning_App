from core.user_activity import User_Activity
from core.user_repository import User_Repository


class Database_Manager:
    def __init__(self):
        self.activity_controller = User_Activity()
        self.user_repo = User_Repository()
        # self.todo_repo = Todo()

    def create_tables(self):
        self.user_repo.create_user_table()
        self.activity_controller.create_activity_table()
        # self.todo_repo.create_todo_table()
