# Generated by Django 4.0.2 on 2022-02-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
