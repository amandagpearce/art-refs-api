from graphene import ObjectType, String, ID, List
from models import (
    Series as SeriesModel,
    MovieScene as MovieSceneModel,
    SeriesScene as SerieSceneModel,
    Movies as MoviesModel,
    Artwork as ArtworksModel,
)
from .schemas import SeriesType, MoviesType, ArtworkAndSceneType


class Query(ObjectType):
    series = List(SeriesType)
    movies = List(MoviesType)

    references = List(
        ArtworkAndSceneType,
        itemId=ID(required=True),
        productionType=String(required=True),
    )

    def resolve_series(self, info):
        return SeriesModel.query.all()

    def resolve_movies(self, info):
        return MoviesModel.query.all()

    def resolve_references(self, info, itemId, productionType):
        combined_references = []

        if productionType == "series":
            # Example: Fetch references for a series
            series_references = SerieSceneModel.query.filter_by(
                seriesId=itemId
            ).all()

            # Extract artworkId values from series_references
            artwork_ids = [ref.artworkId for ref in series_references]

            # Query ArtworksModel to retrieve all info based on artwork_ids
            artworks = ArtworksModel.query.filter(
                ArtworksModel.id.in_(artwork_ids)
            ).all()

            # Combine the references with the corresponding artworks
            for series_ref in series_references:
                for artwork in artworks:
                    if series_ref.artworkId == artwork.id:
                        combined_reference = {
                            "id": artwork.id,
                            "artist": artwork.artist,
                            "artworkTitle": artwork.artworkTitle,
                            "year": artwork.year,
                            "size": artwork.size,
                            "currentLocation": artwork.currentLocation,
                            "description": artwork.description,
                            "imageUrl": artwork.imageUrl,
                            # Add other fields from SeriesceneModel as needed
                            "sceneDescription": series_ref.sceneDescription,
                            "season": series_ref.season,
                            "episode": series_ref.episode,
                        }
                        combined_references.append(combined_reference)

            return combined_references

        elif productionType == "movie":
            # Example: Fetch references for a movie
            movie_references = MovieSceneModel.query.filter_by(
                artworkId=itemId
            ).all()

            # Extract artworkId values from movie_references
            artwork_ids = [ref.artworkId for ref in movie_references]

            # Query ArtworksModel to retrieve all info based on artwork_ids
            artworks = ArtworksModel.query.filter(
                ArtworksModel.id.in_(artwork_ids)
            ).all()

            # Combine the references with the corresponding artworks
            for movie_ref in movie_references:
                for artwork in artworks:
                    if movie_ref.artworkId == artwork.id:
                        combined_reference = {
                            "id": artwork.id,
                            "artist": artwork.artist,
                            "artworkTitle": artwork.artworkTitle,
                            "year": artwork.year,
                            "size": artwork.size,
                            "currentLocation": artwork.currentLocation,
                            "description": artwork.description,
                            "imageUrl": artwork.imageUrl,
                            # Add other fields from MovieSceneModel as needed
                            "sceneDescription": movie_ref.sceneDescription,
                            # Include season and episode if needed
                        }
                        combined_references.append(combined_reference)

            return combined_references

        else:
            # Handle invalid productionType
            return []
