import django
from django.db import models
from django.utils.timezone import now

from django.urls import reverse  # Used to generate URLs by reversing

from django.contrib.auth.models import User
from datetime import date
import uuid,hashlib
import random
import time
def get_unique_str(length):
    uuid_str = str(uuid.uuid4())
    random.seed(time.time())
    offset = random.randrange(1, 30)
    md5 = hashlib.md5()
    random.seed(time.time())
    md5.update(uuid_str.encode('utf-8'))
    return md5.hexdigest()[offset:length+offset]


class user(models.Model):
    userId = models.AutoField(primary_key=True)
    userAlias = models.CharField(max_length=20,unique=True)
    userPwd = models.CharField(max_length=20,default='66666666')
    userPhone = models.CharField(max_length=12,default='13713800000')
    userGender = models.BooleanField(default=True)
    userAvatar = models.FilePathField(path='Avatar/',unique=True)# 具体设置还要查\
    objects = models.manager.QuerySet

    @classmethod
    def create(cls, i,userAvatar=''):
        i = int(i)
        userAlias = get_unique_str(10)
        userPhone = 13713800000+i
        userGender = i%2
        return cls(
            userAlias=userAlias,
            userPhone=str(userPhone),
            userGender = userGender,
            userAvatar = userAvatar,
        )
# likeNum commentNum 函数实现就好

class message(models.Model):
    msId = models.AutoField(primary_key=True)
    #msType = models.CharField(max_length=1,default='3')
    msCx = models.FloatField(default=0)
    msCy = models.FloatField(default=0)
    msUserID = models.CharField(max_length=6)
    # 注意 逻辑上一定要和user表的userId对应！！！
    msText = models.CharField(max_length=144,blank=True,null=True)
    msVoice = models.FilePathField(path='Voice/',blank=True,null=True)
    msLikeCount = models.SmallIntegerField(default=0)
    msDisLikeCount = models.SmallIntegerField(default=0)
    msTime = models.DateTimeField(default=now())
    msCmCount = models.SmallIntegerField(default=0)
    objects = models.manager.QuerySet
    # 需要学习FilePathField
    # FiledField 为啥就能定位到mediaROOT那个文件夹



class like(models.Model):
    likeId = models.AutoField(primary_key=True)

    # 哪位用户给的赞
    likeUserId = models.CharField(max_length=6)

    # 对留言便签给的赞
    likeMsId = models.CharField(max_length=6,null=True)

    likeCmId = models.CharField(max_length=6,null=True)
    likeTime = models.DateTimeField(default=now())

    objects = models.manager.QuerySet


class Dislike(models.Model):
    disLikeId = models.AutoField(primary_key=True)

    # 哪位用户给的赞
    disLikeUserId = models.CharField(max_length=6)

    # 对留言便签给的赞
    disLikeMsId = models.CharField(max_length=6,null=True)

    disLikeCmId = models.CharField(max_length=6,null=True)
    disLikeTime = models.DateTimeField(default=now())
    objects = models.manager.QuerySet


class comment(models.Model):
    cmId = models.AutoField(primary_key = True)
    cmText = models.CharField(max_length=144,default="志之所趋 无远弗届")
    cmUserId = models.CharField(max_length=6)
    cmMsId = models.CharField(max_length=6)
    cmLikeCount = models.SmallIntegerField(default=0)
    cmDisLikeCount = models.SmallIntegerField(default=0)
    cmTime = models.DateTimeField(default=now())
    objects = models.manager.QuerySet
