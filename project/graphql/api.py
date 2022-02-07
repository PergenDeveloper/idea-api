import graphene

from .account.schema import AccountMutations, AccountQueries
from .publication.schema import PublicationMutations, PublicationQueries


class Query(
    AccountQueries,
    PublicationQueries,
    graphene.ObjectType,
):
    pass


class Mutation(
    AccountMutations,
    PublicationMutations,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
