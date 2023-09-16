import graphene
from graphene import ObjectType
import requests
from sqlalchemy import func
import re

from graphene_file_upload.scalars import Upload  # Import the Upload scalar
from graphql import GraphQLError

from artwork.models import Artwork
from series.models import Series, SeriesScene
from movies.models import Movies, MovieScene
from shared.models import artwork_scene_association, References
from shared.types import ReferencesType
from shared.trakt_api import fetch_and_populate
from db import db


class AddInformationMutation(graphene.Mutation):
    class Arguments:
        productionType = graphene.String(required=True)
        productionTitle = graphene.String()
        productionYear = graphene.Int(required=True)

        artist = graphene.String(required=True)
        artworkTitle = graphene.String(required=True)
        artworkDescription = graphene.String()
        artworkYear = graphene.Int()
        size = graphene.String(required=True)
        currentLocation = graphene.String(required=True)

        sceneDescription = graphene.String()
        season = graphene.Int()
        episode = graphene.Int()
        sceneImgUrl = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def retrieve_artwork_url(artworkId, artist, artworkTitle):
        # Make your API call here to retrieve the URL based on artist and artworkTitle
        # Replace the following line with your actual API call
        response = requests.get(
            "http://127.0.0.1:9000/get_image_url",
            params={
                "artist": artist,
                "artworkTitle": artworkTitle,
                "artworkId": artworkId,
            },
        )

        if response.status_code == 200:
            try:
                data = response.json()
                print("data")
                print(data)

                # Check if "imageUrl" is present in the response
                if "imageUrl" in data:
                    # Access and return the "imageUrl" value
                    image_url = data["imageUrl"]
                    return image_url
            except requests.exceptions.JSONDecodeError:
                # Handle the case where the response doesn't contain valid JSON
                print("Invalid JSON response")
        else:
            return None

    def clean_title(title):
        return "".join(e for e in title if e.isalnum()).lower()

    def create_or_get_artwork(
        artist,
        artworkTitle,
        artworkYear,
        size,
        currentLocation,
        artworkDescription,
    ):
        existing_artwork = Artwork.query.filter_by(
            artist=artist, artworkTitle=artworkTitle
        ).first()

        if existing_artwork and existing_artwork.imageUrl:
            print("existing_artwork")
            artwork_id = existing_artwork.id

        elif existing_artwork and not existing_artwork.imageUrl:
            print("existing_artwork without image")
            artwork_id = existing_artwork.id  # Retrieve the artwork ID
            artwork_url = AddInformationMutation.retrieve_artwork_url(
                artwork_id, artist, artworkTitle
            )

            existing_artwork.imageUrl = artwork_url
            db.session.commit()

        else:
            new_artwork = Artwork(
                artist=artist,
                artworkTitle=artworkTitle,
                year=artworkYear,
                size=size,
                currentLocation=currentLocation,
                description=artworkDescription,
            )
            db.session.add(new_artwork)
            db.session.flush()
            artwork_id = new_artwork.id
            artwork_url = AddInformationMutation.retrieve_artwork_url(
                artwork_id, artist, artworkTitle
            )

            print("artwork_url")
            print(artwork_url)

            new_artwork.imageUrl = artwork_url
            db.session.commit()

        return artwork_id

    def create_or_get_production(
        productionType, productionTitle, productionYear
    ):
        # Remove spaces and symbols from the input title
        sanitized_title = AddInformationMutation.clean_title(productionTitle)
        sanitized_title = re.sub(r"[^\w\s]", "", sanitized_title).lower()

        if productionType == "series":
            existing_production = Series.query.filter(
                func.lower(func.replace(Series.productionTitle, " ", ""))
                == sanitized_title,
                Series.year == productionYear,
            ).first()
            print("existing series", existing_production)
        else:
            existing_production = Movies.query.filter(
                func.lower(func.replace(Movies.productionTitle, " ", ""))
                == sanitized_title,
                Movies.year == productionYear,
            ).first()
            print("existing movie", existing_production)

        if existing_production:
            production_id = existing_production.id
            return production_id
        else:
            print("Creating new production...")
            new_production_id = fetch_and_populate(
                productionType, [{"title": productionTitle}]
            )

            if new_production_id is not None:
                print("New production created!")
                production_id = new_production_id
            else:
                print("Error creating new production")
                production_id = None

        return production_id

    def create_scene(
        productionType,
        production_id,
        artwork_id,
        season,
        episode,
        sceneDescription,
        sceneImgUrl,
    ):
        if productionType == "series":
            new_scene = SeriesScene(
                seriesId=production_id,
                artworkId=artwork_id,
                season=season,
                episode=episode,
                sceneDescription=sceneDescription,
                sceneImgUrl=sceneImgUrl,
            )
        else:
            new_scene = MovieScene(
                movieId=production_id,
                artworkId=artwork_id,
                sceneDescription=sceneDescription,
                sceneImgUrl=sceneImgUrl,
            )

        db.session.add(new_scene)
        db.session.commit()

        return new_scene

    def add_to_association(artworkId, sceneId):
        db.session.execute(
            artwork_scene_association.insert().values(
                artworkId=artworkId, sceneId=sceneId
            )
        )
        db.session.commit()

    # @staticmethod
    def mutate(
        self,
        info,
        artist,
        artworkTitle,
        artworkDescription,
        artworkYear,
        size,
        currentLocation,
        productionType,
        productionYear,
        productionTitle=None,
        season=None,
        episode=None,
        sceneDescription=None,
        sceneImgUrl=None,
    ):
        print(productionType)
        if productionType not in ["series", "movie"]:
            return AddInformationMutation(success=False, message="Invalid type")

        artwork_id = AddInformationMutation.create_or_get_artwork(
            artist,
            artworkTitle,
            artworkYear,
            size,
            currentLocation,
            artworkDescription,
        )
        production_id = AddInformationMutation.create_or_get_production(
            productionType, productionTitle, productionYear
        )

        if productionType == "series":
            existing_scene = SeriesScene.query.filter_by(
                seriesId=production_id, artworkId=artwork_id
            ).first()
        else:
            existing_scene = MovieScene.query.filter_by(
                artworkId=artwork_id
            ).first()

        if existing_scene:
            return AddInformationMutation(
                success=False, message="Scene record already exists."
            )

        new_scene = AddInformationMutation.create_scene(
            productionType,
            production_id,
            artwork_id,
            season,
            episode,
            sceneDescription,
            sceneImgUrl,
        )
        AddInformationMutation.add_to_association(artwork_id, new_scene.id)

        return AddInformationMutation(
            success=True, message="Information added successfully"
        )


class AddReferenceToApproveMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        productionType = graphene.String(required=True)
        productionTitle = graphene.String(required=True)
        productionYear = graphene.Int(required=True)
        season = graphene.Int()
        episode = graphene.Int()
        artist = graphene.String(required=True)
        artworkTitle = graphene.String(required=True)
        artworkDescription = graphene.String()
        artworkYear = graphene.Int()
        size = graphene.String()
        currentLocation = graphene.String()
        sceneDescription = graphene.String()
        sceneImgUrl = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(
        self,
        info,
        productionType,
        productionTitle,
        productionYear,
        artist,
        artworkTitle,
        sceneDescription,
        id=None,
        artworkDescription=None,
        season=None,
        episode=None,
        artworkYear=None,
        size=None,
        currentLocation=None,
        sceneImgUrl=None,
    ):
        print("id")
        print(id)
        if id:
            # Check if a record with the provided ID exists in the database
            existing_reference = References.query.get(id)

            print("existing_reference")
            print(existing_reference)

            if existing_reference:
                # Update the existing record with the new values
                existing_reference.productionType = productionType
                existing_reference.productionTitle = productionTitle
                existing_reference.productionYear = productionYear
                existing_reference.season = season
                existing_reference.episode = episode
                existing_reference.artist = artist
                existing_reference.artworkTitle = artworkTitle
                existing_reference.artworkDescription = artworkDescription
                existing_reference.artworkYear = artworkYear
                existing_reference.size = size
                existing_reference.currentLocation = currentLocation
                existing_reference.sceneDescription = sceneDescription

                try:
                    # Commit the changes to the database
                    db.session.commit()

                    message = f"Reference {existing_reference.id} updated successfully"

                    return AddReferenceToApproveMutation(
                        success=True, message=message
                    )
                except Exception as e:
                    # Handle any errors that may occur during the database update
                    return AddReferenceToApproveMutation(
                        success=False,
                        message=f"Error updating reference: {str(e)}",
                    )

        # Create a new reference object
        new_reference = References(
            productionType=productionType,
            productionTitle=productionTitle,
            productionYear=productionYear,
            season=season,
            episode=episode,
            artist=artist,
            artworkTitle=artworkTitle,
            artworkDescription=artworkDescription,
            artworkYear=artworkYear,
            size=size,
            currentLocation=currentLocation,
            sceneDescription=sceneDescription,
            sceneImgUrl=sceneImgUrl,
        )

        try:
            # Save the reference to the database
            db.session.add(new_reference)
            db.session.commit()

            message = f"Reference created successfully. created_reference: {new_reference.id}"

            return AddReferenceToApproveMutation(success=True, message=message)
        except Exception as e:
            # Handle any errors that may occur during the database operation
            return AddReferenceToApproveMutation(
                success=False, message=f"Error creating reference: {str(e)}"
            )


class DeletePendingReferenceMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, id):
        try:
            existing_reference = References.query.get(id)
            if existing_reference:
                # Delete the reference
                db.session.delete(existing_reference)

                # Commit the transaction to apply the deletion
                db.session.commit()

                # Return a success message
                return DeletePendingReferenceMutation(
                    success=True, message="Reference deleted successfully"
                )
            else:
                # Return an error message if the reference was not found
                return DeletePendingReferenceMutation(
                    success=False, message="Reference not found"
                )
        except Exception as e:
            # Handle any errors that may occur during the deletion
            return DeletePendingReferenceMutation(success=False, message=str(e))


# GRAPHIQL EX

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
