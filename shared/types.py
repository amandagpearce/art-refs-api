from graphene import ObjectType, Union, List
from series.types import SeriesSceneType
from movies.types import MovieSceneType


class SceneType(Union):
    class Meta:
        types = (SeriesSceneType, MovieSceneType)
