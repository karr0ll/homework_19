from dao.director import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, did):
        """
        реализует логику получения данных об одном режиссере по его id
        """
        return self.dao.get_one(did)

    def get_all(self):
        """
        реализует логику получения данных обо всех режиссерах
        """
        return self.dao.get_all()

    def create(self, did):
        return self.dao.create(did)

    def update(self, did):
        self.dao.update(did)
        return self.dao

    def delete(self, did):
        self.dao.delete(did)

    def check_and_add_director(self, data):
        """
        проверяет наличие режиссера в таблице
        добавляет нового режиссера, если его нет в таблицe
        """
        all_directors = self.dao.get_all()
        director_name = data.get("director")

        all_director_response = []
        for item in all_directors:
            all_director_response.append(item.name)

        if director_name not in all_director_response:  # if str not in list
            director_max_id = self.dao.get_max_id()
            director_id = director_max_id[1] + 1
            return self.dao.create(director_id, director_name)
