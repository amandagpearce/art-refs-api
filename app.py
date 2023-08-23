import os

from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Schema
from flask_migrate import Migrate
from flask_cors import CORS

from db import db
from models import (
    Artwork as ArtworkModel,
    SeriesReference as SeriesReferenceModel,
)


class Query(ObjectType):
    hello = String()

    def resolve_hello(self, info):
        return "Hello, GraphQL!"


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
        # Define the schema and add the GraphQL route
        schema = Schema(query=Query, mutation=Mutation)
        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view(
                "graphql", schema=schema, graphiql=True
            ),
        )

        db.create_all()  # creating the db

    return app
