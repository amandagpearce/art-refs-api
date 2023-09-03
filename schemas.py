from graphene import ObjectType, String, Int, List, Schema
from graphene_sqlalchemy import SQLAlchemyObjectType
from mutations import AddNewInformationMutation

from models import (
    Series as SeriesModel,
    MovieScene as MovieSceneModel,
    SeriesScene as SeriesceneModel,
    Movies as MoviesModel,
    Artwork as ArtworksModel,
)


class SeriesSceneType(ObjectType):
    id = Int()
    seriesId = Int()
    artworkId = Int()
    sceneDescription = String()


class MovieSceneType(ObjectType):
    id = Int()
    artworkId = Int()
    sceneDescription = String()


class SceneType(ObjectType):
    series_scene = List(SeriesSceneType)
    movie_scene = List(MovieSceneType)


class Series(ObjectType):
    id = Int()
    productionTitle = String()
    year = String()
    imageUrl = String()


class Movies(ObjectType):
    id = Int()
    productionTitle = String()
    year = String()
    imageUrl = String()


class ArtworkType(ObjectType):
    id = Int()
    artworkTitle = String()
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


class Mutation(ObjectType):
    addNewInformation = AddNewInformationMutation.Field()


schema = Schema(query=Query, mutation=Mutation)
