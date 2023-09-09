from shared.mutations import AddInformationMutation
from movies.models import Movies, MovieScene
from shared.models import artwork_scene_association
from db import db


class MoviesMutation(AddInformationMutation):
    def get_existing_production(self, productionTitle):
        return Movies.query.filter_by(productionTitle=productionTitle).first()

    def create_new_production(self, productionTitle):
        new_movie = Movies(productionTitle=productionTitle)
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def get_existing_scene(self, production_id, artworkTitle):
        return MovieScene.query.filter_by(artworkTitle=artworkTitle).first()

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
        new_scene = MovieScene(
            artworkTitle=artworkTitle,
            year=year,
            size=size,
            currentLocation=currentLocation,
            description=description,
            sceneDescription=sceneDescription,
        )

        db.session.add(new_scene)
        db.session.commit()

        return new_scene

    def add_to_association(self, artworkId, sceneId):
        db.session.execute(
            artwork_scene_association.insert().values(
                artworkId=artworkId, sceneId=sceneId
            )
        )
        db.session.commit()
