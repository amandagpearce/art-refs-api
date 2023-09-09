from graphene import ObjectType, String, Int, List
from artwork.types import ArtworkType


class MoviesType(ObjectType):
    id = Int()
    productionTitle = String()
    year = String()
    imageUrl = String()


class MovieSceneType(ObjectType):
    id = Int()
    artworkId = Int()
    sceneDescription = String()
    artworks = List(ArtworkType)
