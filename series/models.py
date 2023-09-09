from db import db
from sqlalchemy import Column, Integer, String


class Series(db.Model):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    productionTitle = Column(String)
    year = Column(Integer)
    imageUrl = Column(String)


class SeriesScene(db.Model):
    __tablename__ = "series_scenes"

    id = db.Column(db.Integer, primary_key=True)
    seriesId = db.Column(
        db.Integer,
        db.ForeignKey("series.id"),
        nullable=False,
    )
    artworkId = db.Column(
        db.Integer, db.ForeignKey("artworks.id"), nullable=False
    )
    sceneDescription = db.Column(db.String, nullable=False)
    season = db.Column(Integer)
    episode = db.Column(Integer)

    # Define the relationship directly to the Artwork model
    artwork = db.relationship("Artwork", back_populates="series_scenes")
