from graphene import ObjectType, Field, List
from series.types import SeriesType
from movies.types import MoviesType
from series.mutations import SeriesMutation
from movies.mutations import MoviesMutation
from series.queries import SeriesQuery
from movies.queries import MoviesQuery


class RootQuery(ObjectType):
    series = Field(
        List(SeriesType),
        resolver=SeriesQuery.resolve_series,  # Make sure to specify the resolver function here
    )
    movies = Field(
        List(MoviesType),
        resolver=MoviesQuery.resolve_movies,
    )
    seriesQuery = Field(SeriesQuery)
    moviesQuery = Field(MoviesQuery)


class RootMutation(ObjectType):
    create_series = Field(
        SeriesMutation
    )  # Use Field to define the SeriesMutation field
    create_movie = Field(MoviesMutation)
