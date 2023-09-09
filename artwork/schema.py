from graphene import ObjectType, String, Int, List


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


class ArtworkAndSceneType(ObjectType):
    id = Int()
    artist = String()
    artworkTitle = String()
    year = Int()
    size = String()
    currentLocation = String()
    description = String()
    imageUrl = String()  # Add the imageUrl field from Artworks table
    # Add fields from either SeriesScenes or MoviesScenes table
    sceneDescription = String()
    season = Int()
    episode = Int()
    # You can add more fields here as needed
