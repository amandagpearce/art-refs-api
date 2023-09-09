from graphene import ObjectType, String, Int, Schema
from series.queries import SeriesQuery


class SeriesSceneType(ObjectType):
    id = Int()
    seriesId = Int()
    artworkId = Int()
    sceneDescription = String()


schema = Schema(query=SeriesQuery)
