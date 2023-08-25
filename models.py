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
    currentLocation = Column(String)
    imageUrl = Column(String)
    scenes = db.relationship(
        "Scene", secondary=artwork_scene_association, back_populates="artworks"
    )


class Series(db.Model):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    imageUrl = Column(String)


class SeriesReferences(db.Model):
    __tablename__ = "seriesReferences"

    id = Column(Integer, primary_key=True)
    seriesId = Column(Integer, ForeignKey("artworks.id"))
    references = Column(Integer, ForeignKey("artworks.id"))

    series = relationship("Artwork", foreign_keys=[seriesId])
    referenced_artwork = relationship("Artwork", foreign_keys=[references])


class Scene(db.Model):
    __tablename__ = "scenes"

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
    artworks = db.relationship(
        "Artwork", secondary=artwork_scene_association, back_populates="scenes"
    )
