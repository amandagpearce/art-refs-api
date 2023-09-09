from db import db


# Intermediary table for many-to-many relationship between artworks and scenes
artwork_scene_association = db.Table(
    "artwork_scene_association",
    db.Column("artworkId", db.Integer, db.ForeignKey("artworks.id")),
    db.Column(
        "sceneId", db.Integer, db.ForeignKey("series_scenes.id")
    ),  # Update to "series_scenes.id"
)
