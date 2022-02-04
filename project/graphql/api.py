import graphene
from .account.schema import AccountQueries, AccountMutations


class Query(
    AccountQueries,
    graphene.ObjectType,
):
    pass


class Mutation(
    AccountMutations,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)