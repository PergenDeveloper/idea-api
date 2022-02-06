
from django.db.models import (
    Exists,
    OuterRef,
    Q,
)
from ...publication import PublicationVisibility, models


def resolve_timeline(info, first, skip):
    requestor = info.context.user
    following = requestor.get_following()

    queryset = models.Publication.objects.all()
    queryset = queryset.filter(
        Q(user=requestor)
        | Q(visibility=PublicationVisibility.PUBLIC)
        | Q(
            Exists(following.filter(following__id=OuterRef("user_id"))),
            visibility=PublicationVisibility.PROTECTED
        ),
    )
    if skip:
        queryset = queryset[skip:]
    if first:
        queryset = queryset[:first]

    return queryset