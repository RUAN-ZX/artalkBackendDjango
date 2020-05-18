import django
from django.db import models
from django.utils.timezone import now

from django.urls import reverse  # Used to generate URLs by reversing

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

# user create
class video(models.Model):
    videoId = models.AutoField(primary_key=True)
    videoTitle = models.CharField(max_length=20,unique=True)
    videoInfo = models.CharField(max_length=200,default='这个Up很懒，没有写简介')
    videoViews = models.IntegerField(default=0)
    videoLikes = models.IntegerField(default=0)
    videoComments = models.IntegerField(default=0)
    videoAnthorId = models.BooleanField(default=True)
    videoTime = models.DateTimeField(default=now())
    # 上传时间
    videoDuration = models.IntegerField(default=60)
    # 时长 秒
    videoUserId = models.CharField(max_length=6)
    # 作者


    # 枚举：
    videoLocation =  models.SmallIntegerField(default=0)
    # 地点 枚举类型！ 0-2

    videoGoal = models.SmallIntegerField(default=0)
    # 目标 0-3

    videoMusucle = models.SmallIntegerField(default=0)
    # 具体肌肉部位 0-7 前面 8-18 后面！

    videoDifficulty = models.SmallIntegerField(default=0)
    # 难易程度 0-5

    videoTool = models.SmallIntegerField(default=0)
    # 锻炼器材 0-3
    objects = models.manager.QuerySet
    @classmethod
    def create(cls, i,videoAvatar=''):
        i = int(i)
        videoAlias = get_unique_str(10)
        videoPhone = 13713800000+i
        videoGender = i%2
        return cls(
            videoAlias=videoAlias,
            videoPhone=str(videoPhone),
            videoGender = videoGender,
            videoAvatar = videoAvatar,
        )


class user(models.Model):
    userId = models.AutoField(primary_key=True)
    userAlias = models.CharField(max_length=20,unique=True)
    userPwd = models.CharField(max_length=20,default='66666666')
    userTime = models.DateTimeField(default=now())
    userPhone = models.CharField(max_length=12,default='13713800000')
    userGender = models.BooleanField(default=True)
    userAvatar = models.FilePathField(path='EdotAuthorAvatar/',unique=True)# 具体设置还要查\
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


class like(models.Model):
    likeId = models.AutoField(primary_key=True)

    # 哪位用户给的赞
    likeUserId = models.CharField(max_length=6)
    # 对视频给的赞
    likeVId = models.CharField(max_length=6,null=True)
    # 只可能二选一 要不对视频要不对评论 点赞
    likeCmId = models.CharField(max_length=6,null=True)
    likeTime = models.DateTimeField(default=now())

    objects = models.manager.QuerySet


class Dislike(models.Model):
    DislikeId = models.AutoField(primary_key=True)

    # 哪位用户给的赞
    DislikeUserId = models.CharField(max_length=6)
    # 对视频给的赞
    DislikeVId = models.CharField(max_length=6,null=True)
    # 只可能二选一 要不对视频要不对评论 点赞
    DislikeCmId = models.CharField(max_length=6,null=True)
    DislikeTime = models.DateTimeField(default=now())

    objects = models.manager.QuerySet


class comment(models.Model):
    cmId = models.AutoField(primary_key = True)
    cmText = models.CharField(max_length=144,default="志之所趋 无远弗届")
    cmUserId = models.CharField(max_length=6)
    cmVId = models.CharField(max_length=6)
    cmLikeCount = models.SmallIntegerField(default=0)
    cmDisLikeCount = models.SmallIntegerField(default=0)
    cmTime = models.DateTimeField(default=now())
    objects = models.manager.QuerySet
