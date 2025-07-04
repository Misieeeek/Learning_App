import json


class Auto_Login:
    def save_logged_in_out_user(self, username=None):
        # IF NONE -> LOGGED OUT
        with open("logged_user.json", "w") as f:
            json.dump({"username": username}, f)

    def load_logged_user(self):
        try:
            with open("logged_user.json", "r") as f:
                data = json.load(f)
                return data.get("username")
        except FileNotFoundError:
            return None
