from django.db import models
from django.utils import timezone
from django.conf import settings

from . import PublicationVisibility


class Publication(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="publications",
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=280)
    visibility = models.CharField(
        max_length=10,
        choices=PublicationVisibility.CHOICES,
        default=PublicationVisibility.PUBLIC
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)