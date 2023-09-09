from graphene import ObjectType, String, ID, Int


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
