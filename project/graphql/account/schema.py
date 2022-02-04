import graphene
from graphql import GraphQLError

from .mutations import AccountRegister
from .types import UserType



class AccountQueries(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged in.')
        return user

class AccountMutations(graphene.ObjectType):
    account_register = AccountRegister.Field()


