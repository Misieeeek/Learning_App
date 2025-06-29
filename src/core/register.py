from core.user_repository import User_Repository


class Register:
    def __init__(self, username, password, confirm_password):
        self.username = username
        self.password = password
        self.confirm_password = confirm_password

    def register_user(self):
        can_register = self.input_correct(
            self.username, self.password, self.confirm_password
        )
        if can_register:
            user_repo = User_Repository()
            user_repo.save_user(self.username, self.password)
        else:
            print("Username/password/confirm password doesn't work")

    def input_correct(self, username, password, confirm_password):
        # CHECK IF USERNAME, PASSWORD, CONFIRM PASSWORD IS NOT NULL
        # AND IF PASSWORD != CONFIRM PASSWORD
        if (
            username == ""
            or password == ""
            or confirm_password == ""
            or password != confirm_password
        ):
            return False
        return True
