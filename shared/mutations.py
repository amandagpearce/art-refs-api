import graphene
import requests

from artwork.models import Artwork
from series.models import Series, SeriesScene
from movies.models import Movies, MovieScene
from shared.models import artwork_scene_association
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
