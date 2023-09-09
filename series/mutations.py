from shared.mutations import AddInformationMutation
from series.models import Series, SeriesScene
from shared.models import artwork_scene_association
from db import db


class SeriesMutation(AddInformationMutation):
    def get_existing_production(self, productionTitle):
        return Series.query.filter_by(productionTitle=productionTitle).first()

    def create_new_production(self, productionTitle):
        new_series = Series(productionTitle=productionTitle)
        db.session.add(new_series)
        db.session.commit()
        return new_series

    def get_existing_scene(self, production_id, artworkTitle):
        return SeriesScene.query.filter_by(
            seriesId=production_id, artworkTitle=artworkTitle
        ).first()

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
        new_scene = SeriesScene(
            seriesId=production_id,
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
