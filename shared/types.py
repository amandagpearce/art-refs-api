from graphene import ObjectType, List
from series.types import SeriesSceneType
from movies.schema import MovieSceneType


class SceneType(ObjectType):
    series_scene = List(SeriesSceneType)
    movie_scene = List(MovieSceneType)
