from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def reset_password_email_task(user_email, link):
    send_mail(
        "Reset password",
        f"This is the link to reset your password: {link}",
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
