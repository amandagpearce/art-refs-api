from db import db
from sqlalchemy import Column, Integer, String


class Movies(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    productionTitle = Column(String)
    year = Column(Integer)
    imageUrl = Column(String)


class MovieScene(db.Model):
    __tablename__ = "movie_scenes"

    id = db.Column(db.Integer, primary_key=True)
    artworkId = db.Column(
        db.Integer, db.ForeignKey("artworks.id"), nullable=False
    )
    sceneDescription = db.Column(db.String, nullable=False)

    # Define the relationship directly to the Artwork model
    artwork = db.relationship("Artwork", back_populates="movie_scenes")
