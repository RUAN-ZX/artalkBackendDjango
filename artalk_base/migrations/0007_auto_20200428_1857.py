# Generated by Django 3.0.2 on 2020-04-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artalk_base', '0006_auto_20200428_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='usrID',
        ),
        migrations.AddField(
            model_name='message',
            name='userID',
            field=models.IntegerField(default=0),
        ),
    ]