# Generated by Django 3.0.2 on 2020-05-19 21:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edotBackend', '0003_auto_20200519_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dislike',
            old_name='DislikeCmId',
            new_name='dislikeCmId',
        ),
        migrations.RenameField(
            model_name='dislike',
            old_name='DislikeId',
            new_name='dislikeId',
        ),
        migrations.RenameField(
            model_name='dislike',
            old_name='DislikeUserId',
            new_name='dislikeUserId',
        ),
        migrations.RenameField(
            model_name='dislike',
            old_name='DislikeVId',
            new_name='dislikeVId',
        ),
        migrations.RemoveField(
            model_name='dislike',
            name='DislikeTime',
        ),
        migrations.AddField(
            model_name='dislike',
            name='dislikeTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 41, 9, 815814)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cmTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 41, 9, 815814)),
        ),
        migrations.AlterField(
            model_name='like',
            name='likeTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 41, 9, 815814)),
        ),
        migrations.AlterField(
            model_name='user',
            name='userTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 41, 9, 814817)),
        ),
        migrations.AlterField(
            model_name='video',
            name='videoTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 41, 9, 814817)),
        ),
    ]
