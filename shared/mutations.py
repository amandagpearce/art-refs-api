import graphene
from graphene import ObjectType
import requests
import boto3
import os
import mimetypes
from botocore.exceptions import NoCredentialsError
from uuid import uuid4
from dotenv import load_dotenv
import threading
import base64
import io

from graphene_file_upload.scalars import Upload  # Import the Upload scalar
from graphql import GraphQLError

from artwork.models import Artwork
from series.models import Series, SeriesScene
from movies.models import Movies, MovieScene
from shared.models import artwork_scene_association, References
from shared.types import ReferencesType
from db import db


class AddInformationMutation(graphene.Mutation):
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
            artwork_url = response.json().get("imageUrl")
            return artwork_url
        else:
            return None

    def create_or_get_artwork(
        artist, artworkTitle, year, size, currentLocation, description
    ):
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
            db.session.flush()
            artwork_id = new_artwork.id
            artwork_url = AddInformationMutation.retrieve_artwork_url(
                artwork_id, artist, artworkTitle
            )
            new_artwork.imageUrl = artwork_url
            db.session.commit()

        return artwork_id

    def create_or_get_production(productionType, productionTitle):
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

        return production_id

    def create_scene(
        productionType,
        production_id,
        artwork_id,
        season,
        episode,
        sceneDescription,
    ):
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
        year,
        size,
        currentLocation,
        description,
        productionType,
        productionTitle=None,
        season=None,
        episode=None,
        sceneDescription=None,
    ):
        print(productionType)
        if productionType not in ["series", "movie"]:
            return AddInformationMutation(success=False, message="Invalid type")

        print("###")
        print("artist")
        print(artist)
        print("artworkTitle")
        print(artworkTitle)
        print("year")
        print(
            year,
        )
        print("size")
        print(size)
        print("currentLocation")
        print(currentLocation)
        print("description")
        print(description)
        print("###")

        artwork_id = AddInformationMutation.create_or_get_artwork(
            artist, artworkTitle, year, size, currentLocation, description
        )
        production_id = AddInformationMutation.create_or_get_production(
            productionType, productionTitle
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
