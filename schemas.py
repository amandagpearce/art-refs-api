import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import (
    Artwork as ArtworkModel,
    SeriesReference as SeriesReferenceModel,
)
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


class Artwork(SQLAlchemyObjectType):
    class Meta:
        model = ArtworkModel


class SeriesReference(SQLAlchemyObjectType):
    class Meta:
        model = SeriesReferenceModel


class Query(graphene.ObjectType):
    artwork = graphene.Field(Artwork, id=graphene.Int())
    all_artworks = SQLAlchemyConnectionField(Artwork)

    def resolve_artwork(self, info, id):
        return Session.query(ArtworkModel).filter_by(id=id).first()


schema = graphene.Schema(query=Query)
