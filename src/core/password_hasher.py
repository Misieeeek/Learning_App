import bcrypt


class Password_Hasher:
    def hash(plain_password):
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def verify(plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
