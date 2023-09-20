from graphene import ObjectType, String, ID, Int, List
from artwork.types import ArtworkType


class SeriesType(ObjectType):
    id = ID()
    productionTitle = String()
    year = String()
    imageUrl = String()


class SeriesSceneType(ObjectType):
    id = Int()
    seriesId = Int()
    artworkId = Int()
    sceneDescription = String()
    sceneImgUrl = String()
    season = Int()
    episode = Int()
    artworks = List(ArtworkType)


class SeriesSearchType(ObjectType):
    title = String()
    year = Int()
