# Generated by Django 4.0.2 on 2022-02-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_rename_active_post_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, default=[], to='core.PostCategory'),
        ),
    ]
