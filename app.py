import os
import subprocess

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
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
    #     "DATABASE_URL",
    #     "sqlite:///database.db",  # default to sqlite if no database_url
    # )
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
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

    return app
