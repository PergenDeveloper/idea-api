import graphene
import graphql_jwt as jwt
from graphql_jwt.decorators import login_required

from .mutations.account import (
    AccountRegister,
    PasswordChange,
    PasswordResetConfirm,
    PasswordResetRequest,
)
from .mutations.follow import (
    FollowAccount,
    FollowAccountConfirm,
    FollowAccountReject,
    FollowerRemove,
    UnfollowAccount,
)
from .resolvers import resolve_search_users
from .types import UserType


class AccountQueries(graphene.ObjectType):
    me = graphene.Field(UserType)
    search_users = graphene.List(
        UserType,
        search=graphene.Argument(graphene.String),
        first=graphene.Argument(graphene.Int),
        skip=graphene.Argument(graphene.Int),
    )

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user

    @login_required
    def resolve_search_users(self, info, search=None, first=None, skip=None, **kwargs):
        return resolve_search_users(search, first, skip)


class AccountMutations(graphene.ObjectType):
    # Account mutations
    account_register = AccountRegister.Field()

    # Token mutations
    token_create = jwt.ObtainJSONWebToken.Field()
    token_verify = jwt.Verify.Field()
    token_refresh = jwt.Refresh.Field()

    # Password mutations
    password_change = PasswordChange.Field()
    password_reset_request = PasswordResetRequest.Field()
    password_reset_confirm = PasswordResetConfirm.Field()

    # Follow mutations
    follow_account = FollowAccount.Field()
    follow_account_confirm = FollowAccountConfirm.Field()
    follow_account_reject = FollowAccountReject.Field()
    unfollow_account = UnfollowAccount.Field()
    follower_remove = FollowerRemove.Field()
