from flask import request

from dao.director import DirectorDAO
from dao.genre import GenreDAO
from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO, genre_dao: GenreDAO, director_dao: DirectorDAO):
        self.dao = dao
        self.genre_dao = genre_dao
        self.director_dao = director_dao

    def create(self, data):
        """
        реализует логику внесния в БД данных о новом фильме
        (принимаются строчные значения жанра и режиссера)
        """

        requested_genre = self.genre_dao.get_genre(data.get("genre"))
        requested_director = self.director_dao.get_director(data.get("director"))

        genre_id = [requested_genre.id for requested_genre in requested_genre]
        director_id = [requested_director.id for requested_director in requested_director]

        id_ = data.get("id")
        title = data.get("title")
        description = data.get("description")
        trailer = data.get("trailer")
        year = data.get("year")
        rating = data.get("rating")
        genre_id = genre_id[0]
        director_id = director_id[0]

        return self.dao.create(id_, title, description, trailer, year, rating, genre_id, director_id)

    def get_one(self, mid):
        """
        реализует логику получения данных об одном фильме по его id
        """
        return self.dao.get_one(mid)

    def get_all(self, director_id=None, genre_id=None, year=None):
        """
        реализует логику получения данных о всех фильмах с фильтрацией по id
        режиссера, жанра, году выпуска
        """
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        year = request.args.get("year")

        if director_id:
            return self.dao.get_all_by_director(director_id)

        if genre_id:
            return self.dao.get_all_by_genre(genre_id)

        if year:
            return self.dao.get_all_by_year(year)

        return self.dao.get_all()

    def update(self, data):
        """
        реализует логику обновления данных об одном фильме по его id
        (принимаются строчные значения жанра и режиссера)
        """
        mid = data.get("id")
        movie = self.get_one(mid)

        requested_genre = self.genre_dao.get_genre(data.get("genre"))
        requested_director = self.director_dao.get_director(data.get("director"))

        genre_id = [requested_genre.id for requested_genre in requested_genre]
        director_id = [requested_director.id for requested_director in requested_director]

        movie.id = mid
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.rating = data.get("rating")
        movie.genre_id = genre_id[0]
        movie.director_id = director_id[0]

        return self.dao.update(movie)

    def delete(self, aid):
        """
        реализует логику удаления данных об одном фильме по его id
        """
        return self.dao.delete(aid)
