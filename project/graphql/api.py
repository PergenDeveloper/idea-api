import graphene
from .account.schema import AccountQueries, AccountMutations
from .publication.schema import PublicationQueries, PublicationMutations


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