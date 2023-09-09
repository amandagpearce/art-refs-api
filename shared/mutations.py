import graphene
import requests
from shared.models import artwork_scene_association
from db import db


class AddInformationMutation(graphene.Mutation):
    class Arguments:
        artist = graphene.String(required=True)
        artworkTitle = graphene.String(required=True)
        year = graphene.Int(required=True)
        size = graphene.String(required=True)
        currentLocation = graphene.String(required=True)
        description = graphene.String(required=True)
        productionTitle = graphene.String(required=True)
        sceneDescription = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def retrieve_artwork_url(artworkId, artist, artworkTitle):
        # retrieve the URL based on artist and artworkTitle
        response = requests.get(
            "http://127.0.0.1:5000/get_image_url",
            params={
                "artist": artist,
                "artworkTitle": artworkTitle,
                "artworkId": artworkId,
            },
        )

        # Check if the API call was successful and extract the artwork_url
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
        artist,
        artworkTitle,
        year,
        size,
        currentLocation,
        description,
        productionTitle,
        sceneDescription,
    ):
        # Check if the series or movie already exists
        existing_production = self.get_existing_production(productionTitle)

        if existing_production:
            production_id = existing_production.id
        else:
            new_production = self.create_new_production(productionTitle)
            production_id = new_production.id

        # Check if a scene with the same production_id and artworkTitle already exists
        existing_scene = self.get_existing_scene(production_id, artworkTitle)

        if existing_scene:
            return self.return_error_message("Scene record already exists.")

        # Create a new scene
        new_scene = self.create_new_scene(
            production_id,
            artworkTitle,
            year,
            size,
            currentLocation,
            description,
            sceneDescription,
        )

        # Now, add the record to the artwork_scene_association table
        self.add_to_association(artworkId=new_scene.id, sceneId=new_scene.id)

        return self.return_success_message("Information added successfully")

    # Methods to be implemented in specific mutations
    def get_existing_production(self, productionTitle):
        raise NotImplementedError()

    def create_new_production(self, productionTitle):
        raise NotImplementedError()

    def get_existing_scene(self, production_id, artworkTitle):
        raise NotImplementedError()

    def create_new_scene(
        self,
        production_id,
        artworkTitle,
        year,
        size,
        currentLocation,
        description,
        sceneDescription,
    ):
        raise NotImplementedError()

    def add_to_association(self, artworkId, sceneId):
        raise NotImplementedError()

    def return_error_message(self, message):
        return AddInformationMutation(success=False, message=message)

    def return_success_message(self, message):
        return AddInformationMutation(success=True, message=message)
