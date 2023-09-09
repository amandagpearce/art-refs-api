import os

from flask import Flask
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_cors import CORS
from graphene import Schema


from trakt_api import fetch_and_populate_series, fetch_and_populate_movies
from db import db
from root_schema import RootMutation, RootQuery


from series.models import Series as SeriesModel
from movies.models import Movies as MoviesModel


def create_app(db_url=None):
    app = Flask(__name__)
    CORS(app)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "ART REFS GRAPHQL API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/doc"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL",
        "sqlite:///database.db",  # default to sqlite if no database_url
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)  # initializes sqlalchemy
    migrate = Migrate(app, db)  # noqa

    with app.app_context():
        db.create_all()  # creating the db

        schema = Schema(query=RootQuery, mutation=RootMutation)

        # Define endpoints for Series and Movies
        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view(
                "graphql", schema=schema, graphiql=True
            ),
        )

        # fetch series from trakt
        if SeriesModel.query.count() == 0:
            fetch_and_populate_series()

        if MoviesModel.query.count() == 0:
            fetch_and_populate_movies()
    return app
