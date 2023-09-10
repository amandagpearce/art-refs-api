from db import db


# Intermediary table for many-to-many relationship between artworks and scenes
artwork_scene_association = db.Table(
    "artwork_scene_association",
    db.Column("artworkId", db.Integer, db.ForeignKey("artworks.id")),
    db.Column(
        "sceneId", db.Integer, db.ForeignKey("series_scenes.id")
    ),  # Update to "series_scenes.id"
)


# table to hold ref data sent from front-end to be approved
class References(db.Model):
    __tablename__ = "refs_to_approve"

    id = db.Column(db.Integer, primary_key=True)
    productionType = db.Column(db.String, nullable=False)
    productionTitle = db.Column(db.String, nullable=False)
    productionYear = db.Column(db.Integer)
    season = db.Column(db.Integer)
    episode = db.Column(db.Integer)
    artist = db.Column(db.String, nullable=False)
    artworkTitle = db.Column(db.String, nullable=False)
    artworkDescription = db.Column(db.String)  # to be inserted upon approval
    artworkYear = db.Column(db.Integer)  # to be inserted upon approval
    size = db.Column(db.String)  # to be inserted upon approval
    currentLocation = db.Column(db.String)  # to be inserted upon approval
    sceneDescription = db.Column(db.String, nullable=False)
    sceneImgUrl = db.Column(db.String)
