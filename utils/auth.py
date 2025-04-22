import bcrypt


def hash_password(plain_password: str):
    return bcrypt.hashpw(plain_password, bcrypt.gensalt(12))


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password, hashed_password)
