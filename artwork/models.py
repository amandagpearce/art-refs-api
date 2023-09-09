from db import db
from sqlalchemy import Column, Integer, String


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
