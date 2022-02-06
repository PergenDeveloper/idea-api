from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from ..account import models as models


@shared_task
def notify_followers_task(username):
    user = (
        models.User.objects.filter(username=username).first()
    )
    for follow in user.get_followers():
        email = follow.follower.email
        send_mail(
            f'New publication.',
            f'{username} has published a new idea.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )