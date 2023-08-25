from graphene import ObjectType, String, Int, List, Schema
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Series as SeriesModel, Scene as SceneModel


class SceneType(ObjectType):
    id = Int()
    seriesId = Int()
    artworkId = Int()
    sceneDescription = String()


class Series(ObjectType):
    id = Int()
    title = String()
    year = String()
    imageUrl = String()


class Query(ObjectType):
    series = List(Series)

    def resolve_series(self, info):
        return SeriesModel.query.all()


schema = Schema(query=Query)
