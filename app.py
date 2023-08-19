from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, String, List, Schema
from flask_pymongo import PyMongo
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/your-database-name"
mongo = PyMongo(app)


if __name__ == "__main__":
    app.run()
