from graphene import ObjectType, Field, List, Int, String

from series.types import SeriesType, SeriesSceneType
from series.queries import SeriesQuery


from movies.types import MoviesType, MovieSceneType
from movies.queries import MoviesQuery

from shared.types import ReferencesType
from shared.queries import ReferencesQuery
from shared.mutations import (
    AddInformationMutation,
    AddReferenceToApproveMutation,
    DeletePendingReferenceMutation,
)


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

    seriesScenes = Field(
        List(SeriesSceneType),
        productionId=Int(),
        productionType=String(required=True),
        resolver=SeriesQuery.resolve_scenes,
    )

    movie_scenes = Field(
        List(MovieSceneType),
        productionId=Int(),
        productionType=String(required=True),
        resolver=MoviesQuery.resolve_scenes,
    )

    references = Field(
        List(ReferencesType),
        resolver=ReferencesQuery.resolve_references,
    )


class RootMutation(ObjectType):
    add_information = (
        AddInformationMutation.Field()
    )  # will get the entire data and distribute across official tables
    create_reference = (
        AddReferenceToApproveMutation.Field()
    )  # will receive frontend form data to be approved
    delete_reference = DeletePendingReferenceMutation.Field()


# mutation {
#   addInformation(
# 		artist: "Frida Kahlo",
#     artworkTitle: "Self-Portrait as a Tehuana",
#     year: 1943,
#     size: "76 cm x 61 cm",
#     currentLocation: "North Carolina Museum of Art",
#     description: "The depth of emotion and symbolism in this artwork is striking. Kahlo\'s gaze is intense and introspective, conveying a sense of self-awareness and resilience. The Tehuana costume becomes a powerful symbol of both her Mexican heritage and her personal struggle with physical and emotional pain. It is within these layers of symbolism that viewers can explore the complexities of Kahlo\'s life and her unapologetic approach to self-representation. \"Self-Portrait as a Tehuana\" continues to resonate with art enthusiasts worldwide, not only for its technical brilliance but also for its ability to evoke a profound sense of empathy and connection with the artist\'s tumultuous life journey.",
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
