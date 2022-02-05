import graphene
import graphql_jwt as jwt
from graphql import GraphQLError

from .mutations import (
    AccountRegister, 
    ConfirmPasswordReset,
    PasswordChange,
    RequestPasswordReset,
)
from .types import UserType



class AccountQueries(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged.')
        return user

class AccountMutations(graphene.ObjectType):
    # Account mutations
    account_register = AccountRegister.Field()

    # Token mutations
    create_token = jwt.ObtainJSONWebToken.Field()
    verify_token = jwt.Verify.Field()
    refresh_token = jwt.Refresh.Field()

    password_change = PasswordChange.Field()
    request_password_reset = RequestPasswordReset.Field()
    confirm_password_reset = ConfirmPasswordReset.Field()


