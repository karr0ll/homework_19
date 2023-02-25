from sqlalchemy import func

from dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """
        загружает список всех жанров
        """
        genres_list = self.session.query(Genre).all()
        return genres_list

    def get_one(self, gid):
        """
        загружает данные одного жанра
        """
        genre = self.session.query(Genre).get(gid)
        return genre

    def get_genre(self, data):
        """
        загружает жанр для дальнейшего получения его id
        """
        genre = self.session.query(Genre).filter(Genre.name == data)
        print(genre)
        return genre


    def get_max_id(self):
        """
        получает последний id
        """
        max_id = self.session.query(Genre, func.max(Genre.id)).one()

        return max_id

    def create(self, genre_id, genre_name):
        """
        создает новый жанр
        """
        new_genre = Genre(
            id=genre_id,
            name=genre_name
        )
        self.session.add(new_genre)
        self.session.commit()
