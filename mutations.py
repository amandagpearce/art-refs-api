import graphene
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
            db.session.commit()
            artwork_id = new_artwork.id

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
