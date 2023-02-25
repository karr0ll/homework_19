import jwt
from flask import request
from flask_restx import abort

from helpers.constants import JWT_SECRET, JWT_ALGORITHM


def auth_required(function):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        return function(*args, **kwargs)

    return wrapper


def auth_admin_required(function):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get("role")
            if role != "admin":
                abort(403)
        except Exception as e:
            print(f"JWT Decode Exception, {e}")
            abort(401)

        return function(*args, **kwargs)

    return wrapper
