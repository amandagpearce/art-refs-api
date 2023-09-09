from graphene import ObjectType, String, Int


class SeriesType(ObjectType):
    id = Int()
    productionTitle = String()
    year = String()
    imageUrl = String()
