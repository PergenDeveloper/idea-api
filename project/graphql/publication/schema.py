import graphene
from graphql_jwt.decorators import login_required

from .mutations import (
    PublicationCreate, 
    PublicationDelete,
    PublicationUpdate,
)
from .types import PublicationType
from .resolvers import resolve_timeline



class PublicationQueries(graphene.ObjectType):
    timeline = graphene.List(
        PublicationType,
        first=graphene.Argument(graphene.Int),
        skip=graphene.Argument(graphene.Int)
    )
    
    @login_required
    def resolve_timeline(self, info, first=None, skip=None, **kwargs):
        return resolve_timeline(info, first, skip)


class PublicationMutations(graphene.ObjectType):
    publication_create = PublicationCreate.Field()
    publication_update = PublicationUpdate.Field()
    publication_delete = PublicationDelete.Field()

