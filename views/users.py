from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import user_schema
from helpers.container import user_service

users_ns = Namespace("users")

@users_ns.route("/")
class UsersView(Resource):
    def get(self):
        users = user_service.get_all()
        response = user_schema.dump(users)

        return response, 200

    def post(self):
        data = request.json
        user = user_service.create(data)
        return "", 201, {"location": f'/users/{user.id}'}




@users_ns.route("/<int:uid>")
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        return user_schema.dump(user), 200

    def put(self, uid):
        data = request.json
        data["id"] = uid
        try:
            user_service.update(data)
            return "", 204
        except Exception as e:
            return str(e), 404


    def delete(self, uid):
        try:
            user_service.delete(uid)
            return "", 204
        except:
            return f" Такой записи в базе нет", 404
