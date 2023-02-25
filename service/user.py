import base64
import hashlib
import hmac

from dao.user import UserDAO
from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_data):
        user_data["password"] = self.generate_hashed_password(user_data["password"])

        return self.dao.create(user_data)

    def delete(self, uid):
        return self.dao.delete(uid)

    def update(self, user_data):
        user_data["password"] = self.generate_hashed_password(user_data["password"])
        return self.dao.update(user_data)

    def generate_hashed_password(self, password):
        hash_pass = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_pass)

    # def compare_passwords(self, password_hash, other_password) -> bool:
    #     return hmac.compare_digest(
    #         base64.b64decode(password_hash),
    #         hashlib.pbkdf2_hmac('sha256', other_password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
    #     )

    def compare_passwords(self, password_hash, received_password):
        decoded_hash_pass = base64.b64decode(password_hash)

        hash_pass = hashlib.pbkdf2_hmac(
            'sha256',
            received_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_hash_pass, hash_pass)
