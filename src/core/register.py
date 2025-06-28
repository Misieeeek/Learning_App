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
            pass

    def input_correct(self, username, password, confirm_password):
        if (
            username == ""
            or password == ""
            or confirm_password == ""
            or password != confirm_password
        ):
            return False
        return True
