# Generated by Django 3.2.6 on 2021-08-11 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]