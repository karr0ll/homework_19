import calendar
import datetime

import jwt
from flask import abort

from helpers.constants import JWT_ALGORITHM, JWT_SECRET
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):

        user = self.user_service.get_by_username(username)
        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }

        token30min = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(token30min.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days10 = datetime.datetime.utcnow() + datetime.timedelta(days=10)
        data["exp"] = calendar.timegm(days10.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        username = data.get("username")

        user = self.user_service.get_by_username(username)
        if user is None:
            raise abort(400)

        return self.generate_tokens(username, user.password, is_refresh=True)
