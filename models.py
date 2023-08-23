from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import db


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


class SeriesReferences(db.Model):
    __tablename__ = "seriesReferences"

    id = Column(Integer, primary_key=True)
    seriesId = Column(Integer, ForeignKey("artworks.id"))
    references = Column(Integer, ForeignKey("artworks.id"))

    series = relationship("Artwork", foreign_keys=[seriesId])
    referenced_artwork = relationship("Artwork", foreign_keys=[references])
