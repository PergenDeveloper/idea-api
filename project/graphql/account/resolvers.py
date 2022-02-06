from django.db.models import (
    Exists,
    OuterRef,
    Q,
)
from ...publication import PublicationVisibility
from ...account.models import User

def resolve_search_users(info, search, first, skip):
    users = User.objects.all()
    if search:
        users = users.filter(username__icontains=search)
    if skip:
        users = users[skip:]
    if first:
        users = users[:first]

    return users


def resolve_publications(info, user, first, skip):
    requestor = info.context.user
    if user != requestor:
        follows = requestor.get_following()
        publications = user.publications.filter(
            Q(visibility=PublicationVisibility.PUBLIC)
            | Q(
                Exists(follows.filter(following__id=OuterRef("user_id"))), 
                visibility=PublicationVisibility.PROTECTED
            ),
        )
    else:
        publications = user.publications.all()
    if skip:
        publications = publications[skip:]
    if first:
        publications = publications[:first]
    return publications


def resolve_following(root, first, skip):
    following = root.get_following()
    users = User.objects.filter(
        Exists(following.filter(following__id=OuterRef("pk"))),
    )
    if skip:
        users = users[skip:] 
    if first:
        users = users[:first] 
    return users

def resolve_followers(root, first, skip):
    followers = root.get_followers()
    users = User.objects.filter(
        Exists(followers.filter(follower__id=OuterRef("pk"))),
    )

    if skip:
        users = users[skip:] 
    if first:
        users = users[:first] 
    return users

def resolve_follower_requests(root, first, skip):
    followers_request = root.get_follower_requests()
    users = User.objects.filter(
        Exists(followers_request.filter(follower__id=OuterRef("id"))),
    )

    if skip:
        users = users[skip:] 
    if first:
        users = users[:first] 
    return users

