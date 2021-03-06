# Generated by Django 3.1 on 2020-05-20 00:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edotBackend', '0008_auto_20200520_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='cmTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 20, 0, 57, 51, 495948)),
        ),
        migrations.AlterField(
            model_name='dislike',
            name='disLikeTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 20, 0, 57, 51, 495425)),
        ),
        migrations.AlterField(
            model_name='like',
            name='likeTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 20, 0, 57, 51, 495046)),
        ),
        migrations.AlterField(
            model_name='user',
            name='userTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 20, 0, 57, 51, 494580)),
        ),
        migrations.AlterField(
            model_name='video',
            name='videoTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 20, 0, 57, 51, 493908)),
        ),
    ]
