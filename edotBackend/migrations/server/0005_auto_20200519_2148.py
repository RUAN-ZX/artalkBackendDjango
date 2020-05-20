# Generated by Django 3.0.2 on 2020-05-19 21:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edotBackend', '0004_auto_20200519_2141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dislike',
            old_name='dislikeCmId',
            new_name='disLikeCmId',
        ),
        migrations.RenameField(
            model_name='dislike',
            old_name='dislikeId',
            new_name='disLikeId',
        ),
        migrations.RenameField(
            model_name='dislike',
            old_name='dislikeUserId',
            new_name='disLikeUserId',
        ),
        migrations.RenameField(
            model_name='dislike',
            old_name='dislikeVId',
            new_name='disLikeVId',
        ),
        migrations.RemoveField(
            model_name='dislike',
            name='dislikeTime',
        ),
        migrations.AddField(
            model_name='dislike',
            name='disLikeTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 48, 30, 215762)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cmTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 48, 30, 216794)),
        ),
        migrations.AlterField(
            model_name='like',
            name='likeTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 48, 30, 215762)),
        ),
        migrations.AlterField(
            model_name='user',
            name='userTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 48, 30, 215762)),
        ),
        migrations.AlterField(
            model_name='video',
            name='videoTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 48, 30, 215762)),
        ),
    ]
