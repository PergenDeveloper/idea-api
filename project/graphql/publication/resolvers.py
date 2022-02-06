
from django.db.models import (
    Exists,
    OuterRef,
    Q,
)
from ...publication.models import Publication
from ...publication import PublicationVisibility



def resolve_timeline(info, first, skip):
    requestor = info.context.user
    following = requestor.get_following()

    publications = (
        Publication.objects.filter(
            Q(user=requestor)
            | Q(visibility=PublicationVisibility.PUBLIC)
            | Q(
                Exists(following.filter(following__id=OuterRef("user_id"))),
                visibility=PublicationVisibility.PROTECTED
            ),
        )
    )
    if skip:
        publications = publications[skip:]
    if first:
        publications = publications[:first]

    return publications