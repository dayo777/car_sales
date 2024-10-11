# import bcrypt
# from main import config
#
#
# def hash_password(password: str) -> str:
#     """Return a salted password hash."""
#     return bcrypt.hashpw(password.encode(), config["SALT"]).decode()