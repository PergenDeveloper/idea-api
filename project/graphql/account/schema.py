import graphene
import graphql_jwt as jwt
from graphql import GraphQLError

from ..publication.types import PublicationType
from .mutations import (
    AccountRegister, 
    ConfirmPasswordReset,
    FollowAccount,
    FollowAccountConfirm,
    FollowAccountReject,
    FollowerRemove,
    PasswordChange,
    RequestPasswordReset,
    UnfollowAccount,
)
from .types import UserType
from .resolvers import resolve_search_users



class AccountQueries(graphene.ObjectType):
    me = graphene.Field(UserType)
    search_users = graphene.List(
        UserType,
        search=graphene.Argument(graphene.String),
        first=graphene.Argument(graphene.Int),
        skip=graphene.Argument(graphene.Int)
    )
    timeline = graphene.List(
        PublicationType,
        first=graphene.Argument(graphene.Int),
        skip=graphene.Argument(graphene.Int)
    )

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged.')
        return user
    
    def resolve_search_users(self, info, search=None, first=None, skip=None, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged.')
        return resolve_search_users(info, search, first, skip)


class AccountMutations(graphene.ObjectType):
    # Account mutations
    account_register = AccountRegister.Field()

    # Token mutations
    create_token = jwt.ObtainJSONWebToken.Field()
    verify_token = jwt.Verify.Field()
    refresh_token = jwt.Refresh.Field()

    # Password mutations
    password_change = PasswordChange.Field()
    request_password_reset = RequestPasswordReset.Field()
    confirm_password_reset = ConfirmPasswordReset.Field()

    # Follow mutations
    follow_account = FollowAccount.Field()
    follow_account_confirm = FollowAccountConfirm.Field()
    follow_account_reject = FollowAccountReject.Field()
    unfollow_account = UnfollowAccount.Field()
    follower_remove = FollowerRemove.Field()


