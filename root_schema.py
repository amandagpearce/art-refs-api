from graphene import ObjectType, Field, List

from series.types import SeriesType


from movies.types import MoviesType
from series.queries import SeriesQuery
from movies.queries import MoviesQuery

from shared.mutations import AddInformationMutation


class RootQuery(ObjectType):
    series = Field(
        List(SeriesType),
        resolver=SeriesQuery.resolve_series,
    )
    movies = Field(
        List(MoviesType),
        resolver=MoviesQuery.resolve_movies,
    )
    seriesQuery = Field(SeriesQuery)
    moviesQuery = Field(MoviesQuery)


class RootMutation(ObjectType):
    add_information = AddInformationMutation.Field()


# mutation {
#   addInformation(
# 		artist: "Frida Kahlo",
#     artworkTitle: "Self-Portrait as a Tehuana",
#     year: 1943,
#     size: "76 cm x 61 cm",
#     currentLocation: "North Carolina Museum of Art",
#     description: "The original piece, Kahlo’s Self Portrait as a Tehuana...",
#     productionType: "series",
#     productionTitle: "Euphoria",
#     season: 2,
#     episode: 4,
#     sceneDescription: "Jules recreates a famous work of art by Frida Kahlo, appearing with a portrait of love interest Rue painted on her forehead."
#   ) {
#     success
#     message
#   }
# }
