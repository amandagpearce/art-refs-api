from graphene import ObjectType, String, ID, List
from artwork.models import Artwork as ArtworksModel
from artwork.types import ArtworkAndSceneType
from series.models import Series as SeriesModel
from series.models import SeriesScene as SeriesSceneModel
from series.types import SeriesType


class SeriesQuery(ObjectType):
    series = List(SeriesType)

    def resolve_series(self, info):
        print("##### SeriesModel.query.all()")
        print(SeriesModel.query.all())
        print("########################")

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
