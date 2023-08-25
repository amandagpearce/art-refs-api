import os

from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Schema, List
from flask_migrate import Migrate
from flask_cors import CORS

from models import (
    Series as SeriesModel,
)
from trakt_api import fetch_and_populate_series
from db import db
from schemas import schema


class Query(ObjectType):
    series = List(SeriesModel)  # GraphQL query to fetch series

    def resolve_series(self, info):
        return SeriesModel.query.all()


class Mutation(ObjectType):
    add_todo = String(task=String())

    def resolve_add_todo(self, info, task):
        return f"Added task: {task}"


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
        # Define the GraphQL route
        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view(
                "graphql", schema=schema, graphiql=True
            ),
        )

        # fetch series from trakt
        if SeriesModel.query.count() == 0:
            fetch_and_populate_series()

    return app
