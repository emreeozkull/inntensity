# Generated by Django 5.2 on 2025-04-11 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_artist_performer_remove_event_artist_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='artist',
            new_name='performer',
        ),
    ]
