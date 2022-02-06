import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from ...publication import models, tasks
from ..publication.enums import PublicationVisibilityEnum
from ..publication.types import PublicationType


class PublicationCreateInput(graphene.InputObjectType):
    text = graphene.String(required=True, description="Text of publication.")
    visibility = graphene.Field(
        PublicationVisibilityEnum,
        required=True
    )


class PublicationUpdateInput(graphene.InputObjectType):
    text = graphene.String(required=False, description="Text of publication.")
    visibility = graphene.Field(
        PublicationVisibilityEnum,
        required=False
    )


class PublicationCreate(graphene.Mutation):
    publication = graphene.Field(PublicationType)

    class Arguments:
        input = PublicationCreateInput(
            required=True,
            description="Fields required to create a publication."
        )

    @classmethod
    @login_required
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        data = kwargs.get('input')
        
        publication = models.Publication(
            user=user,
            **data
        )
        publication.save()

        # Notify followers
        tasks.notify_followers_task.delay(user.username)

        return cls(publication=publication)


class PublicationUpdate(graphene.Mutation):
    publication = graphene.Field(PublicationType)

    class Arguments:
        id = graphene.UUID(
            required=True,
             description="ID of publication."
        )
        input = PublicationUpdateInput(
            required=True,
            description="Fields required to create a publication."
        )

    @classmethod
    @login_required
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        id = kwargs.get('id')
        data = kwargs.get('input')

        publication = user.publications.filter(uuid=id).first()

        if not publication:
            raise GraphQLError('Publication not found.')
        
        publication.text = data.get("text", publication.text)
        publication.visibility = data.get("visibility", publication.visibility)
        publication.save(update_fields=['text', 'visibility'])

        return cls(publication=publication)



class PublicationDelete(graphene.Mutation):
    publication = graphene.Field(PublicationType)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.UUID(
            required=True,
            description="ID of publication."
        )

    @classmethod
    @login_required
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        id = kwargs.get('id')

        publication = user.publications.filter(uuid=id).first()

        if not publication:
            raise GraphQLError('Publication not found.')
        
        publication.delete()

        return cls(publication=publication, deleted=True)