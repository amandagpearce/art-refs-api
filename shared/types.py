from graphene import ObjectType, Union, Int, String
from series.types import SeriesSceneType
from movies.types import MovieSceneType


class SceneType(Union):
    class Meta:
        types = (SeriesSceneType, MovieSceneType)


class ReferencesType(ObjectType):
    id = Int()
    productionType = String()
    productionTitle = String()
    productionYear = Int()
    season = Int()
    episode = Int()
    artist = String()
    artworkTitle = String()
    artworkDescription = String()
    artworkYear = Int()
    size = String()
    currentLocation = String()
    sceneDescription = String()
    sceneImgUrl = String()
