# Generated by Django 3.2.12 on 2022-02-05 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0002_publication_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ('-created_at',)},
        ),
    ]
