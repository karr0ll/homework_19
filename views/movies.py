from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import movies_schema, movie_schema
from helpers.container import movie_service, genre_service, director_service
from helpers.decorators import auth_required, auth_admin_required

movies_ns = Namespace('movies')


@movies_ns.route("/")
class MoviesView(Resource):
    @auth_required
    def get(self):
        """
        получает все фильмы
        """
        try:
            all_movies = movie_service.get_all()

            return movies_schema.dump(all_movies), 200
        except Exception as e:
            return str(e), 404

    @auth_admin_required
    def post(self):
        """
        добавляет новый фильм
        """
        try:
            request_json = request.json
            genre_service.check_and_add_genre(request_json)
            director_service.check_and_add_director(request_json)
            movie = movie_service.create(request_json)

            return "", 201, {"location": f"/movies/{request_json['id']}"}

        except Exception as e:
            return str(e), 404


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid: int):
        """
        получает один фильм по его id
        """
        try:
            movie = movie_service.get_one(mid)

            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    @auth_admin_required
    def put(self, mid: int):
        """
        обновляет один фильм по его id
        """
        data = request.json
        data["id"] = mid
        try:
            genre_service.check_and_add_genre(data)
            director_service.check_and_add_director(data)
            movie_service.update(data)

            return "", 200

        except Exception as e:
            return str(e), 404

    @auth_admin_required
    def delete(self, mid: int):
        """
        удаляет один фильм по его id
        """
        try:
            movie_service.delete(mid)
            return "", 204
        except:
            return f" Такой записи в базе нет", 404
