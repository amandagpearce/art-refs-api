from graphene import ObjectType, String, Int, List, Schema
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import (
    Series as SeriesModel,
    Scene as SceneModel,
    Movies as MoviesModel,
    Artwork as ArtworksModel,
)


class SceneType(ObjectType):
    id = Int()
    series_id = Int()
    artwork_id = Int()
    scene_description = String()


class Series(ObjectType):
    id = Int()
    title = String()
    year = String()
    imageUrl = String()


class Movies(ObjectType):
    id = Int()
    title = String()
    year = String()
    imageUrl = String()


class ArtworkType(ObjectType):
    id = Int()
    title = String()
    year = Int()
    artist = String()
    size = String()
    description = String()
    current_location = String()
    imageUrl = String()
    scenes = List("SceneType")


class Query(ObjectType):
    series = List(Series)
    movies = List(Movies)

    def resolve_series(self, info):
        return SeriesModel.query.all()

    def resolve_movies(self, info):
        return MoviesModel.query.all()


schema = Schema(query=Query)
