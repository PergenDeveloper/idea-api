
import graphene
from graphene_django import DjangoObjectType

from ...publication import models
from ..publication.enums import PublicationVisibilityEnum


class PublicationType(DjangoObjectType):
    id = graphene.UUID()
    username = graphene.String()
    visibility = graphene.Field(PublicationVisibilityEnum)

    class Meta:
        model = models.Publication
        fields = (
            "id",
            'text',
            'created_at'
        )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related('user')

    def resolve_username(root: models.Publication, info, **kwargs):
        return root.user.username

    def resolve_visibility(root: models.Publication, info, **kwargs):
        return PublicationVisibilityEnum[root.visibility]

    def resolve_id(root: models.Publication, info, **kwargs):
        return root.uuid