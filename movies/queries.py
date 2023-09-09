from graphene import ObjectType, ID, List
from artwork.models import Artwork as ArtworksModel
from artwork.types import ArtworkAndSceneType
from movies.models import Movies as MoviesModel, MovieScene as MovieSceneModel
from movies.types import MoviesType


class MoviesQuery(ObjectType):
    movies = List(MoviesType)

    references = List(ArtworkAndSceneType, itemId=ID(required=True))

    def resolve_movies(self, info):
        return MoviesModel.query.all()

    def resolve_scenes(self, info, itemId):
        combined_references = []

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
                        "sceneDescription": movie_ref.sceneDescription,
                    }
                    combined_references.append(combined_reference)

        return combined_references
