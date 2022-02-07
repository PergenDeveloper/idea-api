import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from . import FollowStatus


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """Create a user instance with the given email, username and password."""
        values = [
            email,
            username,
        ]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError(f"The {field_name} value must be set")

        email = UserManager.normalize_email(email)

        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        return self.create_user(
            email, username, password, is_staff=True, is_superuser=True, **extra_fields
        )


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    def get_followers(self):
        if not hasattr(self, "followers"):
            return []
        return self.followers.select_related("follower").filter(
            status=FollowStatus.ACCEPTED
        )

    def get_following(self):
        if not hasattr(self, "following"):
            return []
        return self.following.select_related("following").filter(
            status=FollowStatus.ACCEPTED
        )

    def get_follower_requests(self):
        if not hasattr(self, "followers"):
            return []
        return self.followers.select_related("follower").filter(
            status=FollowStatus.PENDING
        )


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=10, choices=FollowStatus.CHOICES, default=FollowStatus.PENDING
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        unique_together = (
            "follower",
            "following",
        )

    def __str__(self) -> str:
        return f"{self.follower} -> {self.following}"


class OneTimeToken(models.Model):
    user = models.ForeignKey(
        User, related_name="one_time_tokens", on_delete=models.CASCADE
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    valid = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.token
