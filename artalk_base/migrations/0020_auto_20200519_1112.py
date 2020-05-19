# Generated by Django 3.0.2 on 2020-05-19 11:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artalk_base', '0019_auto_20200518_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='cmTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 11, 12, 13, 161424)),
        ),
        migrations.AlterField(
            model_name='dislike',
            name='disLikeTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 11, 12, 13, 160464)),
        ),
        migrations.AlterField(
            model_name='like',
            name='likeTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 11, 12, 13, 160464)),
        ),
        migrations.AlterField(
            model_name='message',
            name='msTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 11, 12, 13, 160464)),
        ),
        migrations.AlterField(
            model_name='message',
            name='msVoice',
            field=models.FilePathField(blank=True, null=True, path='artalk/Voice/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='userAvatar',
            field=models.FilePathField(path='artalk/Avatar/', unique=True),
        ),
    ]
