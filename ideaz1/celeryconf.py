import logging
import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings


CELERY_LOGGER_NAME = "celery"


@setup_logging.connect
def setup_celery_logging(loglevel=None, **kwargs):
    """Skip default Celery logging configuration.
    Will rely on Django to set up the base root logger.
    Celery loglevel will be set if provided as Celery command argument.
    """
    if loglevel:
        logging.getLogger(CELERY_LOGGER_NAME).setLevel(loglevel)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ideaz1.settings")

app = Celery("saleor")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


