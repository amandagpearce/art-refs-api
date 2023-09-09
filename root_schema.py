from graphene import ObjectType, Field, List, Int, String

from series.types import SeriesType, SeriesSceneType
from series.queries import SeriesQuery


from movies.types import MoviesType, MovieSceneType
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

    series_scenes = Field(
        List(SeriesSceneType),
        productionId=Int(),
        productionType=String(required=True),
        resolver=SeriesQuery.resolve_scenes,  # Assuming SeriesQuery has a resolver for series scenes
    )

    movie_scenes = Field(
        List(MovieSceneType),
        productionId=Int(),
        productionType=String(required=True),
        resolver=MoviesQuery.resolve_scenes,  # Assuming MoviesQuery has a resolver for movie scenes
    )


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
