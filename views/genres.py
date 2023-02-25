from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import genre_schema, genres_schema
from helpers.container import genre_service
from helpers.decorators import auth_required, auth_admin_required

genres_ns = Namespace('genres')


@genres_ns.route("/")
class GenresView(Resource):
    @auth_required
    def get(self):
        """
        получает все жанры
        """
        try:
            all_genres = genre_service.get_all()
            return genres_schema.dump(all_genres), 200
        except Exception as e:
            return str(e), 404

    @auth_admin_required
    def post(self):
        try:
            request_json = request.json
            genre_service.create(request_json)
            return "", 201, {"location": f"/directors/{request_json['id']}"}
        except Exception as e:
            return str(e), 404


@genres_ns.route("/<int:gid>")
class GenresView(Resource):
    @auth_required
    def get(self, gid: int):
        """
        получает один жанр по его id
        """
        try:
            genre = genre_service.get_one(gid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    @auth_admin_required
    def put(self, did: int):
        data = request.json
        data["id"] = did
        try:
            genre_service.update(data)
            return "", 200

        except Exception as e:
            return str(e), 404

    @auth_admin_required
    def delete(self, did: int):
        try:
            genre_service.delete(did)
            return "", 204
        except:
            return f" Такой записи в базе нет", 404
