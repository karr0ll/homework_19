from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import directors_schema, director_schema
from helpers.container import director_service
from helpers.decorators import auth_required, auth_admin_required


directors_ns = Namespace('directors')


@directors_ns.route("/")
class DirectorsView(Resource):
        @auth_required
        def get(self):
            """
            получает всех режиссеров
            """
            try:
                all_directors = director_service.get_all()
                return directors_schema.dump(all_directors), 200
            except Exception as e:
                return str(e), 404

        @auth_admin_required
        def post(self):
            try:
                request_json = request.json
                director_service.create(request_json)
                return "", 201, {"location": f"/directors/{request_json['id']}"}
            except Exception as e:
                return str(e), 404

@directors_ns.route("/<int:did>")
class DirectorsView(Resource):
    @auth_required
    def get(self, did: int):
        """
        получает одного режиссера по его id
        """
        try:
            director = director_service.get_one(did)
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    @auth_admin_required
    def put(self, did: int):
        data = request.json
        data["id"] = did
        try:
            director_service.update(data)
            return "",200

        except Exception as e:
            return str(e), 404

    @auth_admin_required
    def delete(self, did: int):
        try:
            director_service.delete(did)
            return "", 204
        except:
            return f" Такой записи в базе нет", 404

