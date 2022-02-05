from typing import Dict
import django
import graphene
from graphql import GraphQLError

from django.conf import settings
from django.db import transaction

from ...account import models
from ...account import tasks
from ...utils.validators import valid_email_format, valid_password, valid_username_format
from .types import UserType


class AccountRegisterInput(graphene.InputObjectType):
    email = graphene.String(required=True, description="Email of user.")
    username = graphene.String(required=True, description="Username of user.")
    password = graphene.String(required=True, description="Password of user.")


class PasswordChangeInput(graphene.InputObjectType):
    old_password = graphene.String(required=True, description="Old password of user.")
    new_password = graphene.String(required=True, description="New password of user.")


class AccountRegister(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = AccountRegisterInput(
            required=True,
            description="Fields required to create an user."
        )

    @classmethod
    def clean_input(cls, info, data: Dict):
        """Returns the input data after all checks and cleanups."""

        email = data.get('email', '').lower()
        username = data.get('username', '').lower()

        if not valid_email_format(email):
            raise GraphQLError('This email is not valid.')

        if models.User.objects.filter(email=email).exists():
            raise GraphQLError('This email already exists.')
            
        if not valid_username_format(username):
            raise GraphQLError('The username provided is not valid.')
        
        if models.User.objects.filter(username=username).exists():
            raise GraphQLError('This username already exists.')
        
        if not valid_password(data['password']):
            raise GraphQLError(
                'Invalid password. Must be at least 8 characters.'
            )

        data["email"], data["username"] = email, username
        return data

    @classmethod
    def mutate(cls, _, info, **kwargs):
        cleaned_data = cls.clean_input(info, kwargs.get('input'))
        password = cleaned_data.pop("password")
        
        user = models.User(**cleaned_data)
        user.set_password(password)
        user.save()

        return cls(user=user)



class PasswordChange(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = PasswordChangeInput(
            required=True,
            description="Fields required to create an user."
        )

    @classmethod
    def clean_input(cls, user, data: Dict):
        """Returns the input data after all checks and cleanups."""

        if not user.check_password(data['old_password']):
            raise GraphQLError('Old password is not valid.')

        if not valid_password(data['new_password']):
            raise GraphQLError(
                'Invalid new password. Must be at least 8 characters.'
            )

        return data

    @classmethod
    def mutate(cls, _, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged.')

        cleaned_data = cls.clean_input(user, kwargs.get('input'))
        password = cleaned_data.pop("new_password")

        user.set_password(password)
        user.save()

        return cls(user=user)



class RequestPasswordReset(graphene.Mutation):
    requested = graphene.Boolean()

    class Arguments:
        email = graphene.String(
            required=True,
            description="Email of user where we will send the magic link."
        )

    @classmethod
    def generate_magic_link(cls, token):
        return f'{settings.MAIN_DOMAIN}/reset-password/?token={token}'

    @classmethod
    def mutate(cls, _, info, **kwargs):
        email = kwargs.get("email")
        user = models.User.objects.filter(email=email).first()
        if not user:
            raise GraphQLError('This email not exists in our system.') 

        # If token already exists, return this one.
        onetimetoken = (
            models.OneTimeToken
            .objects.filter(user=user, valid=True)
            .first()
        )
        if not onetimetoken:
            onetimetoken = models.OneTimeToken(user=user)
            onetimetoken.save()

        link = cls.generate_magic_link(onetimetoken.token)

        # Send reset password email
        tasks.reset_password_email_task.delay(email, link)

        return cls(requested=True)


class ConfirmPasswordReset(graphene.Mutation):
    confirmed = graphene.Boolean()

    class Arguments:
        token = graphene.String(
            required=True,
            description="Email of user where we will send the magic link."
        )
        password = graphene.String(
            required=True,
            description="New password of user."
        )

    @classmethod
    def mutate(cls, _, info, **kwargs):
        token = kwargs.get("token")
        password = kwargs.get("password")
        onetimetoken = (
            models.OneTimeToken.objects
            .select_related('user')
            .filter(token=token, valid=True,)
            .first()
        )

        if not onetimetoken:
            raise GraphQLError('This token is not valid.')

        if not valid_password(password):
            raise GraphQLError(
                'Invalid password. Must be at least 8 characters.'
            )

        with transaction.atomic():
            user = onetimetoken.user
            onetimetoken.valid = False
            onetimetoken.save()

            user.set_password(password)
            user.save()

        return cls(confirmed=True)