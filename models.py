from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import db

# Intermediary table for many-to-many relationship between artworks and scenes
artwork_scene_association = db.Table(
    "artwork_scene_association",
    db.Column("artwork_id", db.Integer, db.ForeignKey("artworks.id")),
    db.Column("scene_id", db.Integer, db.ForeignKey("scenes.id")),
)


class Artwork(db.Model):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    artist = Column(String)
    size = Column(String)
    description = Column(String)
    current_location = Column(String)
    image_url = Column(String)
    scenes = db.relationship(
        "Scene", secondary=artwork_scene_association, back_populates="artworks"
    )


class Series(db.Model):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    image_url = Column(String)


class Movies(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    image_url = Column(String)


class SeriesReferences(db.Model):
    __tablename__ = "series_references"

    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey("artworks.id"))
    references = Column(Integer, ForeignKey("artworks.id"))

    series = relationship("Artwork", foreign_keys=[series_id])
    referenced_artwork = relationship("Artwork", foreign_keys=[references])


class Scene(db.Model):
    __tablename__ = "scenes"

    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(
        db.Integer,
        db.ForeignKey("series.id"),
        nullable=False,
    )
    artwork_id = db.Column(
        db.Integer, db.ForeignKey("artworks.id"), nullable=False
    )
    scene_description = db.Column(db.String, nullable=False)
    artworks = db.relationship(
        "Artwork", secondary=artwork_scene_association, back_populates="scenes"
    )
