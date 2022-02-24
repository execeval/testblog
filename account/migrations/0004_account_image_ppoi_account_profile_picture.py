# Generated by Django 4.0.2 on 2022-02-22 11:16

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_account_is_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='image_ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20),
        ),
        migrations.AddField(
            model_name='account',
            name='profile_picture',
            field=versatileimagefield.fields.VersatileImageField(null=True, upload_to='images', verbose_name='Image'),
        ),
    ]
