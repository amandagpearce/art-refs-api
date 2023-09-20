import os
from dotenv import load_dotenv
from graphene import ObjectType, String, ID, List
import requests
import json

from artwork.models import Artwork as ArtworksModel
from artwork.types import ArtworkAndSceneType
from series.models import Series as SeriesModel
from series.models import SeriesScene as SeriesSceneModel
from series.types import SeriesType, SeriesSearchType


class SeriesQuery(ObjectType):
    series = List(SeriesType)

    def resolve_series(self, info):
        return SeriesModel.query.all()

    references = List(
        ArtworkAndSceneType,
        itemId=ID(required=True),
        productionType=String(required=True),
    )

    def resolve_scenes(self, info, productionType, productionId):
        combined_references = []

        if productionType == "series":
            # Example: Fetch references for a series
            series_references = SeriesSceneModel.query.filter_by(
                seriesId=productionId
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
                            "id": series_ref.id,  # Use series_ref.id for scene id
                            "sceneDescription": series_ref.sceneDescription,
                            "sceneImgUrl": series_ref.sceneImgUrl,
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
                            "season": series_ref.season,
                            "episode": series_ref.episode,
                        }
                        combined_references.append(combined_reference)

        # Handle cases where no scenes are found
        if not combined_references:
            return None

        return combined_references


class SearchSeriesQuery(ObjectType):
    searchSeries = List(SeriesSearchType, searchTerm=String(required=True))

    def resolve_search_series(self, info, searchTerm):
        load_dotenv()
        trakt_api_key = os.getenv("TRAKT_API_KEY")

        trakt_api_url = f"https://api.trakt.tv/search/show?query={searchTerm}"

        headers = {
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": trakt_api_key,
        }

        response = requests.get(trakt_api_url, headers=headers)

        if response.status_code == 200:
            series_data = response.json()

            # Filter the series_data to only include results where searchTerm appears in show.title
            filtered_series_data = [
                item["show"]
                for item in series_data
                if "show" in item
                and searchTerm.lower() in item["show"]["title"].lower()
            ]

            final_series_data = [
                {"title": item["title"], "year": item["year"]}
                for item in filtered_series_data
            ]

            pretty_series_data = json.dumps(final_series_data, indent=4)
            print("series_data", pretty_series_data)

            # Return a list of SeriesSearchType
            return [SeriesSearchType(**result) for result in final_series_data]

        return []
