import bcrypt


class Password_Hasher:
    def hash(self, plain_password):
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def verify(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
