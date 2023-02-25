from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gid):
        """
        реализует логику получения данных об одном жанре по его id
        """
        return self.dao.get_one(gid)

    def get_all(self):
        """
        реализует логику получения данных обо всех жанрах
        """
        return self.dao.get_all()

    def create(self, gid):
        return self.dao.create(gid)

    def update(self, gid):
        self.dao.update(gid)
        return self.dao

    def delete(self, gid):
        self.dao.delete(gid)

    def check_and_add_genre(self, data):
        """
        проверяет наличие жанра в таблице
        добавляет новый жанр, если его нет в таблицe
        """
        all_genres = self.dao.get_all()
        genre_name = data.get("genre")

        all_genres_response = []
        for item in all_genres:
            all_genres_response.append(item.name)

        if genre_name not in all_genres_response:
            genre_max_id = self.dao.get_max_id()
            genre_id = genre_max_id[1] + 1
            return self.dao.create(genre_id, genre_name)
