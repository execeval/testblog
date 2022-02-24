# Generated by Django 4.0.2 on 2022-02-23 13:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_rename_post_postreaction_xost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postreaction',
            old_name='xost',
            new_name='post',
        ),
        migrations.AlterUniqueTogether(
            name='postreaction',
            unique_together={('author', 'post')},
        ),
    ]
