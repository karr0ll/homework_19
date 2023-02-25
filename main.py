from flask import Flask
from flask_restx import Api

from config import Config
from dao.model.user import User
from helpers.container import user_service
from setup_db import db
from views.auth import auth_ns
from views.directors import directors_ns
from views.genres import genres_ns
from views.movies import movies_ns
from views.users import users_ns


def create_app(config: Config):
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application


def configure_app(application):
    db.init_app(application)

    api = Api(application)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)
    create_table(application, db)


def create_table(application, db):
    with application.app_context():
        with db.session.begin():
            db.create_all()

        u1 = User(username="vasya", password=user_service.generate_hashed_password("my_little_pony"), role="user")
        u2 = User(username="olegu", password=user_service.generate_hashed_password("qwerty"), role="user")
        u3 = User(username="olega", password=user_service.generate_hashed_password("P@ssw0rd"), role="admin")

        db.session.add_all([u1, u2, u3])
        db.session.commit()


app_config = Config()
app = create_app(app_config)
configure_app(app)

if __name__ == '__main__':
    app.run()
