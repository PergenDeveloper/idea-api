import graphene
from graphene_django import DjangoObjectType

from ...account import models
from ..publication.types import PublicationType
from .resolvers import (
    resolve_follower_requests,
    resolve_followers,
    resolve_following,
    resolve_publications,
)


class UserType(DjangoObjectType):
    followers = graphene.List(
        lambda: UserType,
        first=graphene.Argument(graphene.Int),
        skip=graphene.Argument(graphene.Int),
    )
    following = graphene.List(
        lambda: UserType,
        first=graphene.Argument(graphene.Int),
        skip=graphene.Argument(graphene.Int),
    )
    follower_requests = graphene.List(
        lambda: UserType,
        first=graphene.Argument(graphene.Int),
        skip=graphene.Argument(graphene.Int),
    )
    publications = graphene.List(
        PublicationType,
        first=graphene.Argument(graphene.Int),
        skip=graphene.Argument(graphene.Int),
    )

    class Meta:
        model = models.User
        fields = (
            "email",
            "username",
        )

    def resolve_followers(root: models.User, info, first=None, skip=None, **kwargs):
        if info.context.user != root:
            return None
        return resolve_followers(root, first, skip)

    def resolve_following(root: models.User, info, first=None, skip=None, **kwargs):
        if info.context.user != root:
            return None
        return resolve_following(root, first, skip)

    def resolve_follower_requests(
        root: models.User, info, first=None, skip=None, **kwargs
    ):
        if info.context.user != root:
            return None
        return resolve_follower_requests(root, first, skip)

    def resolve_publications(root: models.User, info, first=None, skip=None, **kwargs):
        return resolve_publications(info, root, first, skip)


class FollowType(DjangoObjectType):
    class Meta:
        model = models.Follow
