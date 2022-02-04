import graphene
from graphene_django import DjangoObjectType
from ...account import models

class UserType(DjangoObjectType):
    followers = graphene.List(lambda: UserType)
    following = graphene.List(lambda: UserType)
    follower_requests = graphene.List(lambda: UserType)

    class Meta:
        model = models.User
        only_fields = (
            'email',
            'username',
        )

    def resolve_followers(root: models.User, info, **kwargs):
        if info.context.user != root:
            return None
        return root.get_followers()

    def resolve_following(root: models.User, info, **kwargs):
        if info.context.user != root:
            return None
        return root.get_following()

    def resolve_follower_requests(root: models.User, info, **kwargs):
        if info.context.user != root:
            return None
        return root.get_follower_requests()


class FollowType(DjangoObjectType):
    class Meta:
        model = models.Follow