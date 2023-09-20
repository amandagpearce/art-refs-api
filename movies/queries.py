import os
from dotenv import load_dotenv
from graphene import ObjectType, String, ID, List
import requests
import json

from artwork.models import Artwork as ArtworksModel
from artwork.types import ArtworkAndSceneType
from movies.models import Movies as MoviesModel, MovieScene as MovieSceneModel
from movies.types import MoviesType, MoviesSearchType


class MoviesQuery(ObjectType):
    movies = List(MoviesType)

    references = List(
        ArtworkAndSceneType,
        itemId=ID(required=True),
        productionType=String(required=True),
    )

    def resolve_movies(self, info):
        return MoviesModel.query.all()

    def resolve_scenes(self, info, productionType, productionId):
        combined_references = []

        if productionType == "movie":
            movie_references = MovieSceneModel.query.filter_by(
                movieId=productionId
            ).all()

            print("movie_references", movie_references)

            # Extract artworkId values from movie_references
            artwork_ids = [ref.artworkId for ref in movie_references]
            print("artwork_ids", artwork_ids)

            # Query ArtworksModel to retrieve all info based on artwork_ids
            artworks = ArtworksModel.query.filter(
                ArtworksModel.id.in_(artwork_ids)
            ).all()

            print("artworks", artworks)

            # Combine the references with the corresponding artworks
            for movie_ref in movie_references:
                for artwork in artworks:
                    if movie_ref.artworkId == artwork.id:
                        combined_reference = {
                            "id": artwork.id,
                            "sceneDescription": movie_ref.sceneDescription,
                            "sceneImgUrl": movie_ref.sceneImgUrl,
                            "artworks": [  # Create a list of artworks
                                {
                                    "id": artwork.id,
                                    "artist": artwork.artist,
                                    "artworkTitle": artwork.artworkTitle,
                                    "year": artwork.year,
                                    "size": artwork.size,
                                    "currentLocation": artwork.currentLocation,
                                    "description": artwork.description,
                                    "imageUrl": artwork.imageUrl,
                                }
                            ],
                        }
                        combined_references.append(combined_reference)

            return combined_references


class SearchMoviesQuery(ObjectType):
    searchMovies = List(MoviesSearchType, searchTerm=String(required=True))

    def resolve_search_movies(self, info, searchTerm):
        load_dotenv()
        trakt_api_key = os.getenv("TRAKT_API_KEY")

        trakt_api_url = f"https://api.trakt.tv/search/movie?query={searchTerm}"

        headers = {
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": trakt_api_key,
        }

        response = requests.get(trakt_api_url, headers=headers)

        if response.status_code == 200:
            movies_data = response.json()

            filtered_movies_data = [
                item["movie"]
                for item in movies_data
                if "movie" in item
                and searchTerm.lower() in item["movie"]["title"].lower()
            ]

            final_movies_data = [
                {"title": item["title"], "year": item["year"]}
                for item in filtered_movies_data
            ]

            pretty_series_data = json.dumps(final_movies_data, indent=4)
            print("movies_data", pretty_series_data)

            # Return a list of SeriesSearchType
            return [MoviesSearchType(**result) for result in final_movies_data]

        return []
