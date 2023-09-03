from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import db

# Intermediary table for many-to-many relationship between artworks and scenes
artwork_scene_association = db.Table(
    "artwork_scene_association",
    db.Column("artworkId", db.Integer, db.ForeignKey("artworks.id")),
    db.Column(
        "sceneId", db.Integer, db.ForeignKey("series_scenes.id")
    ),  # Update to "series_scenes.id"
)


class Artwork(db.Model):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True)
    artworkTitle = Column(String)
    year = Column(Integer)
    artist = Column(String)
    size = Column(String)
    description = Column(String)
    currentLocation = Column(String)
    imageUrl = Column(String)

    # Relationship to represent referenced series scenes
    series_scenes = db.relationship("SeriesScene", back_populates="artwork")

    # Relationship to represent referenced movie scenes
    movie_scenes = db.relationship("MovieScene", back_populates="artwork")


class Series(db.Model):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    productionTitle = Column(String)
    year = Column(Integer)
    imageUrl = Column(String)


class Movies(db.Model):
    __tablename__ = "movies"

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


class MovieScene(db.Model):
    __tablename__ = "movie_scenes"

    id = db.Column(db.Integer, primary_key=True)
    artworkId = db.Column(
        db.Integer, db.ForeignKey("artworks.id"), nullable=False
    )
    sceneDescription = db.Column(db.String, nullable=False)

    # Define the relationship directly to the Artwork model
    artwork = db.relationship("Artwork", back_populates="movie_scenes")
