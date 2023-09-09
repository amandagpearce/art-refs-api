import graphene
import requests
from models import (
    Artwork,
    Series,
    Movies,
    SeriesScene,
    MovieScene,
    artwork_scene_association,
)
from db import db


class AddNewInformationMutation(graphene.Mutation):
    class Arguments:
        productionType = graphene.String(required=True)
        artist = graphene.String(required=True)
        artworkTitle = graphene.String(required=True)
        year = graphene.Int(required=True)
        size = graphene.String(required=True)
        currentLocation = graphene.String(required=True)
        description = graphene.String(required=True)
        productionTitle = graphene.String()
        season = graphene.Int()
        episode = graphene.Int()
        sceneDescription = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    # Function to make the API call and retrieve the URL
    @staticmethod
    def retrieve_artwork_url(artworkId, artist, artworkTitle):
        # Make your API call here to retrieve the URL based on artist and artworkTitle
        # Replace the following line with your actual API call
        response = requests.get(
            "http://127.0.0.1:5000/get_image_url",
            params={
                "artist": artist,
                "artworkTitle": artworkTitle,
                "artworkId": artworkId,
            },
        )

        # Check if the API call was successful
        if response.status_code == 200:
            # Assuming your API response contains the URL, extract it
            artwork_url = response.json().get("imageUrl")

            print("artwork_url")
            print(artwork_url)

            return artwork_url
        else:
            # Handle the case where the API call fails
            return None

    def mutate(
        self,
        info,
        productionType,
        artist,
        artworkTitle,
        year,
        size,
        currentLocation,
        description,
        productionTitle=None,
        season=None,
        episode=None,
        sceneDescription=None,
    ):
        # Check if type is valid
        if productionType not in ["series", "movie"]:
            return AddNewInformationMutation(
                success=False, message="Invalid type"
            )

        # Check if the artwork already exists
        existing_artwork = Artwork.query.filter_by(
            artist=artist, artworkTitle=artworkTitle
        ).first()

        if existing_artwork:
            artwork_id = existing_artwork.id
        else:
            new_artwork = Artwork(
                artist=artist,
                artworkTitle=artworkTitle,
                year=year,
                size=size,
                currentLocation=currentLocation,
                description=description,
            )
            db.session.add(new_artwork)
            db.session.flush()  # Use flush instead of commit to get the id
            artwork_id = new_artwork.id
            artwork_url = AddNewInformationMutation.retrieve_artwork_url(
                artwork_id, artist, artworkTitle
            )

            print("artwork_url")
            print(artwork_url)

            # Set the imageUrl attribute with the retrieved artwork_url
            new_artwork.imageUrl = artwork_url

            db.session.commit()  # Commit the changes after retrieving the id and setting the imageUrl

        # Check if the series or movie already exists
        if productionType == "series":
            existing_production = Series.query.filter_by(
                productionTitle=productionTitle
            ).first()
        else:
            existing_production = Movies.query.filter_by(
                productionTitle=productionTitle
            ).first()

        if existing_production:
            production_id = existing_production.id
        else:
            if productionType == "series":
                new_production = Series(productionTitle=productionTitle)
            else:
                new_production = Movies(productionTitle=productionTitle)

            db.session.add(new_production)
            db.session.commit()
            production_id = new_production.id

        # Check if a scene with the same production_id already exists
        if productionType == "series":
            existing_scene = SeriesScene.query.filter_by(
                seriesId=production_id, artworkId=artwork_id
            ).first()
        else:
            existing_scene = MovieScene.query.filter_by(
                artworkId=artwork_id
            ).first()

        if existing_scene:
            return AddNewInformationMutation(
                success=False, message="Scene record already exists."
            )

        # Create a new scene
        if productionType == "series":
            new_scene = SeriesScene(
                seriesId=production_id,
                artworkId=artwork_id,
                season=season,
                episode=episode,
                sceneDescription=sceneDescription,
            )
        else:
            new_scene = MovieScene(
                artworkId=artwork_id,
                sceneDescription=sceneDescription,
            )

        db.session.add(new_scene)
        db.session.commit()

        # Now, add the record to the artwork_scene_association table
        db.session.execute(
            artwork_scene_association.insert().values(
                artworkId=artwork_id, sceneId=new_scene.id
            )
        )
        db.session.commit()

        return AddNewInformationMutation(
            success=True, message="Information added successfully"
        )


# mutation {
#   addNewInformation(
#     artist: "Frida Kahlo",
#     artworkTitle: "Self-Portrait as a Tehuana",
#     year: 1943,
#     size: "76 cm x 61 cm",
#     currentLocation: "North Carolina Museum of Art",
#     description: "The original piece, Kahlo’s Self Portrait as a Tehuana, was painted the year of her divorce from fellow artist and ex-husband Diego Rivera and is said to be symbolic of her inability to stop thinking about him. It goes by two other names: Diego in My Thoughts and Thinking of Diego, and presumably makes reference to the intense dynamic between Jules and Rue in the show.",
#     productionTitle: "Euphoria",
#     season: 2,
#     episode: 4,
#     productionType: "series",
#     sceneDescription: "Jules recreates a famous work of art by Frida Kahlo, appearing with a portrait of love interest Rue painted on her forehead."
#   ) {
#     success
#     message
#   }
# }
