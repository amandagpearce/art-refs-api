from graphene import ObjectType, String, ID, List
from shared.types import ReferencesType
from shared.models import References as ReferencesModel


class ReferencesQuery(ObjectType):
    references = List(ReferencesType)

    def resolve_references(self, info):
        return ReferencesModel.query.all()
