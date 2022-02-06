import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from ....account.models import User, Follow
from ....account import FollowStatus


class FollowAccount(graphene.Mutation):
    followed = graphene.Boolean()

    class Arguments:
        username = graphene.String(
            required=True,
            description="Username of user to follow."
        )

    @classmethod
    @login_required
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        username = kwargs.get("username")

        if user.username == username:
             raise GraphQLError('You can not follow yourself.')

        user_to_follow = (
            User.objects.filter(username=username).first()
        )

        if not user_to_follow:
            raise GraphQLError("User with this username doesn't exists.")

        if Follow.objects.filter(follower=user, following=user_to_follow).exists():
            raise GraphQLError("You can not follow a user twice.")

        Follow.objects.create(
            follower=user,
            following=user_to_follow
        )

        return cls(followed=True)


class UnfollowAccount(graphene.Mutation):
    unfollowed = graphene.Boolean()

    class Arguments:
        username = graphene.String(
            required=True,
            description="Username of user to unfollow."
        )

    @classmethod
    @login_required
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        username = kwargs.get("username")

        follow = Follow.objects.filter(
            follower=user, 
            following__username=username
        ).first()

        if not follow:
            raise GraphQLError("You are not following this user.")

        follow.delete()

        return cls(unfollowed=True)


class FollowAccountConfirm(graphene.Mutation):
    follow_confirmed = graphene.Boolean()

    class Arguments:
        username = graphene.String(
            required=True,
            description="Username of user to follow."
        )

    @classmethod
    @login_required
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        username = kwargs.get("username")

        follow = Follow.objects.filter(
            follower__username=username,
            following=user,
            status=FollowStatus.PENDING
        ).first()

        if not follow:
            raise GraphQLError("This user not follow you.")

        follow.status = FollowStatus.ACCEPTED
        follow.save(update_fields=['status'])

        return cls(follow_confirmed=True)


class FollowAccountReject(graphene.Mutation):
    follow_rejected = graphene.Boolean()

    class Arguments:
        username = graphene.String(
            required=True,
            description="Username of user to follow."
        )

    @classmethod
    @login_required
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        username = kwargs.get("username")

        follow = Follow.objects.filter(
            follower__username=username,
            following=user,
            status=FollowStatus.PENDING
        ).first()

        if not follow:
            raise GraphQLError("The follow of this user is not pending or not exists.")

        follow.delete()

        return cls(follow_rejected=True)


class FollowerRemove(graphene.Mutation):
    follower_removed = graphene.Boolean()

    class Arguments:
        username = graphene.String(
            required=True,
            description="Username of user to follow."
        )

    @classmethod
    @login_required
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        username = kwargs.get("username")

        follow = Follow.objects.filter(
            follower__username=username,
            following=user,
            status=FollowStatus.ACCEPTED
        ).first()

        if not follow:
            raise GraphQLError("This user not follow you.")

        follow.delete()

        return cls(follower_removed=True)
