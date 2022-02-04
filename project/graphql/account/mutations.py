import graphene
from graphql import GraphQLError
from ...account import models
from ...core.validators import validate_email, validate_username
from .types import UserType

class AccountRegisterInput(graphene.InputObjectType):
    email = graphene.String(required=True, description="Email of user")
    username = graphene.String(required=True, description="Username of user")
    password = graphene.String(required=True, description="Password of user")


class AccountRegister(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = AccountRegisterInput(
            required=True,
            description="Fields required to create a user."
        )

    def mutate(_, info, **kwargs):
        data = kwargs.get('input')

        email = data.get('email', '').lower()
        username = data.get('username', '').lower()
        password = data.get("password")

        if not validate_email(email):
            raise GraphQLError('This email is not valid.')
            
        if not validate_username(username):
            raise GraphQLError('The username provided is not valid.')
        
        user = models.User(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save()
        
        return AccountRegister(user=user)