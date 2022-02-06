from django.db.models import (
    Exists,
    OuterRef,
    Q,
)
from ...publication import PublicationVisibility
from ...account import models

def resolve_search_users(info, search, first, skip):
    queryset = models.User.objects.all()
    if search:
        queryset = queryset.filter(username__icontains=search)
    if skip:
        queryset = queryset[skip:]
    if first:
        queryset = queryset[:first]

    return queryset


def resolve_publications(info, user, first, skip):
    requestor = info.context.user
    if user != requestor:
        following = requestor.get_following()
        queryset = user.publications.filter(
            Q(visibility=PublicationVisibility.PUBLIC)
            | Q(
                Exists(following.filter(following__id=OuterRef("user_id"))), 
                visibility=PublicationVisibility.PROTECTED
            ),
        )
    else:
        queryset = user.publications.all()
    if skip:
        queryset = queryset[skip:]
    if first:
        queryset = queryset[:first]
    return queryset


def resolve_following(root, first, skip):
    following = root.get_following()
    qs = models.User.objects.filter(
        Exists(following.filter(following__id=OuterRef("pk"))),
    )
    if skip:
        qs = qs[skip:] 
    if first:
        qs = qs[:first] 
    return qs

def resolve_followers(root, first, skip):
    followers = root.get_followers()
    qs = models.User.objects.filter(
        Exists(followers.filter(follower__id=OuterRef("pk"))),
    )

    if skip:
        qs = qs[skip:] 
    if first:
        qs = qs[:first] 
    return qs

def resolve_follower_requests(root, first, skip):
    followers_request = root.get_follower_requests()
    qs =  models.User.objects.filter(
        Exists(followers_request.filter(follower__id=OuterRef("pk"))),
    )

    if skip:
        qs = qs[skip:] 
    if first:
        qs = qs[:first] 
    return qs

