from graphene import ObjectType, String, Int, Schema
from movies.queries import MoviesQuery


class MovieSceneType(ObjectType):
    id = Int()
    artworkId = Int()
    sceneDescription = String()


schema = Schema(query=MoviesQuery)
