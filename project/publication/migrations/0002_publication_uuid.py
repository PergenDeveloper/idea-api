# Generated by Django 3.2.12 on 2022-02-05 19:02

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("publication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
