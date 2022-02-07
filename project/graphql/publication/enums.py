import graphene

from ...publication import PublicationVisibility

PublicationVisibilityEnum = graphene.Enum(
    "PublicationVisibilityEnum",
    [(code, code) for code, _ in PublicationVisibility.CHOICES],
)
