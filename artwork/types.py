from graphene import ObjectType, String, Int, List, ID


class ArtworkType(ObjectType):
    id = ID()
    artworkTitle = String()
    year = Int()
    artist = String()
    size = String()
    description = String()
    current_location = String()
    imageUrl = String()


class ArtworkAndSceneType(ObjectType):
    id = ID()
    artist = String()
    artworkTitle = String()
    year = Int()
    size = String()
    currentLocation = String()
    description = String()
    imageUrl = String()
    sceneDescription = String()
    season = Int()
    episode = Int()
