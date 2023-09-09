from graphene import ObjectType, String, Int


class MoviesType(ObjectType):
    id = Int()
    productionTitle = String()
    year = String()
    imageUrl = String()
