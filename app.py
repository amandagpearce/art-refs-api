import os

from flask import Flask, g, request
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_cors import CORS
from graphene import Schema
import json


from shared.trakt_api import fetch_and_populate
from db import db
from shared.root_schema import RootMutation, RootQuery


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
    db.init_app(app)  # initializes SQLAlchemy
    # migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()  # creating the database tables

        schema = Schema(query=RootQuery, mutation=RootMutation)

        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view(
                "graphql",
                schema=schema,
                graphiql=True,
                context={"parsed_operations": None},
            ),
            methods=["GET", "POST"],
        )

        # Populate Series and Movies with initial data
        if SeriesModel.query.count() == 0:
            predefined_series = [
                {"title": "Euphoria", "year": 2019},
                {"title": "The Simpsons", "year": 1987},
                {"title": "Squid Game", "year": 2021},
                {"title": "The Queen’s Gambit", "year": 2020},
                {"title": "BoJack Horseman", "year": 2014},
                {"title": "Futurama", "year": 1999},
                {"title": "Family Guy", "year": 1999},
                {"title": "Hannibal", "year": 2013},
                {"title": "Succession", "year": 2018},
            ]
            print("Populating series table...")
            fetch_and_populate("series", predefined_series)

        if MoviesModel.query.count() == 0:
            predefined_movies = [
                {"title": "Shirley: Visions of Reality", "year": 2013},
                {"title": "Cabaret", "year": 1972},
                {"title": "The Dreamers", "year": 2003},
                {"title": "A Clockwork Orange", "year": 1971},
                {"title": "About Schmidt", "year": 2002},
                {"title": "The Fifth Element", "year": 1997},
                {"title": "Shutter Island", "year": 2010},
                {"title": "Passion", "year": 2012},
                {"title": "Mad Max Fury Road", "year": 2015},
                {"title": "Forrest Gump", "year": 1994},
            ]

            print("Populating movies table...")
            fetch_and_populate("movie", predefined_movies)

    return app
