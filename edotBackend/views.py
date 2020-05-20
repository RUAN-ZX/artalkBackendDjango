import os
import random
from time import time
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import uuid,hashlib
from .models import video, user,comment,like,Dislike
import json

videoInfoList = [
    "“波比跳”一般指波比运动，是一种常见的健身运动。Burpee(波比)是一种高强度，短时间燃烧脂肪，令人心跳率飙升的自重阻力训练动作之一，也叫作立卧撑跳。",
    "根据科学研究表明，平均每30千克肌肉在静止的状态下每天消耗1500卡路里，即使您什么都不做。一年下来您的肌肉组织能消耗大约550000卡路里。",
    "Burpees波比跳结合了深蹲、俯卧撑、屈腿收腹、跳跃等训练的复合动作，因此会训练到全身70%以上的肌肉群，包含核心肌群、脚、手臂、腹部、臀部及背部等",
    "如果运动时间超过一个小时，请喝运动饮料，补充体内流失的微量元素如电解质",
    "这个世界上，取得成功的人是那些努力寻找他们想要机会的人，如果找不到机会，他们就去创造机会。",
    "有氧负责减重！力量负责塑形！想要最大限度燃烧脂肪，两者结合更佳哦！",
    "健身前一小时，不要吃不易消化的食品（油脂类、肉类、酒类），可以吃适当的碳水化合物",
    "器械训练时尽量不要长时间憋气，动作要慢，体会肌肉的发力（憋气容易让体内压力增加造成内脏出血）",
    "训练后不要立即洗澡，以免造成体内湿气无法排除；洗澡时水温不宜过高，以免造成免疫力下降",
    "切忌盲目攀比，一看别人推胸20KG，你也来，要知道死亡率最高的动作就是卧推，你训练的目的是刺激肌肉的生长，而不是跟别人攀比",
    "挑你喜欢的运动，没有最好的只有适合自己的，只有喜欢才能长久坚持！",
]
CommentList = [
    "运动后第二天肌肉酸痛是正常反应",
    "你所谓的岁月静好，是因为有人在负重前行",
    "训练后30分钟不要抽烟，血液加速循环促进尼古丁的吸收",
    "训练后不要立即洗澡，以免造成体内湿气无法排除；洗澡时水温不宜过高，以免造成免疫力下降",
    "锻炼期间不要喝碳酸饮料！",
    "知不足，然后能自反也；知困，然后能自强也。",
    "有氧训练由缓慢开始，也该由缓慢结束。跑完步不要立马停下，走几分钟！",
    "锻炼前不吃辛辣刺激食物",
    "保证充足的睡眠（8小时）",
    "隔一段时间改变自己的训练计划，身体适应性很强，不改变，进步会变慢或者进入平台期",
    "锻炼不是越累越好，看目标肌群是否被锻炼到，看是否有泵感！",
]

def get_unique_str(length):
    uuid_str = str(uuid.uuid4())
    random.seed(time())
    offset = random.randrange(1, 30)
    md5 = hashlib.md5()
    random.seed(time())
    md5.update(uuid_str.encode('utf-8'))
    return md5.hexdigest()[offset:length+offset]

def ValidationPk(modelI,id):
    # 小心get的问题！
    #if model.objects==models.manager.QuerySet:
        if modelI.objects.filter(pk=id):
            return 1
        else:
            return 0

def transform(a):
    if(a==True):
        return 3
    elif(a==False):
        return 2
    else:
        return 1

def getRandomDisLikeUser(code,id):

    userI = user.objects.all()[random.randrange(0,int( user.objects.count()))].userId
    # 当code=1 是给message点赞
    if code:
        # CmId 为空 那么msId就有值了
        if not bool(Dislike.objects.filter(Q(disLikeUserId=userI)&Q(disLikeVId=id)))&bool(like.objects.filter(Q(likeUserId=userI)&Q(likeVId=id))):
            return userI
        else:
            return getRandomDisLikeUser(code,id)
    # 是为了comment点赞：
    else:
        if not bool(Dislike.objects.filter(Q(disLikeCmId=id)&Q(disLikeUserId=userI)))&bool(like.objects.filter(Q(likeUserId=userI)&Q(likeCmId=id))):
            return userI
        else:
            return getRandomDisLikeUser(code,id)


def getRandomLikeUser(code,id):
    # 假设目前有30用户！
    userI = user.objects.all()[random.randrange(0,int( user.objects.count()))].userId
    # 当code=1 是给message点赞
    if code:
        # CmId 为空 那么msId就有值了
        if not bool(like.objects.filter(Q(likeVId=id) & Q(likeUserId=userI)))&bool(Dislike.objects.filter(Q(disLikeVId=id) & Q(disLikeUserId=userI))):
            return userI
        else:
            return getRandomLikeUser(code,id)
    # 是为了comment点赞：
    else:
        #print('22')
        if not bool(like.objects.filter(Q(likeCmId=id) & Q(likeUserId=userI)))&bool(Dislike.objects.filter(Q(disLikeCmId=id) & Q(disLikeUserId=userI))):
            return userI
        else:
            return getRandomLikeUser(code,id)
# videoId = models.AutoField(primary_key=True)
# videoTitle = models.CharField(max_length=20,unique=True)
# videoInfo = models.CharField(max_length=200,default='这个Up很懒，没有写简介')
# videoViews = models.IntegerField(default=0)
# videoLikes = models.IntegerField(default=0)
# videoComments = models.IntegerField(default=0)
# videoTime = models.DateTimeField(default=now())
# # 上传时间
# videoDuration = models.IntegerField(default=60)
# # 时长 秒
# videoUserId = models.CharField(max_length=6)
# # 作者
#
#
# # 枚举：
# videoLocation =  models.SmallIntegerField(default=0)
# # 地点 枚举类型！ 0-2
# videoGoal = models.SmallIntegerField(default=0)
# # 目标 0-3
# videoMusucle = models.SmallIntegerField(default=0)
# # 具体肌肉部位 0-7 前面 8-17 后面！
# videoDifficulty = models.SmallIntegerField(default=0)
# # 难易程度 0-5
# videoTool = models.SmallIntegerField(default=0)
def getVideo(request):
    if request.method == "POST":
        try:
            # 具体视频显示页面
            mId = int(request.POST.get('Id'))
            videoI = video.objects.get(videoId=mId)

            # 基本信息
            videoTitle = videoI.videoTitle
            videoInfo = videoI.videoInfo
            videoTime = videoI.videoTime
            videoSrc = videoI.videoSrc
            # 离线的时候可能需要封面？
            videoCover = videoI.videoCover
            # 上传视频的时候存封面

            # 时长可以通过 上传video的时候就获取到了 存数据库就好
            videoDuration = videoI.videoDuration

            # like dislike comment Counts!
            videoLikes = videoI.videoLikes
            videoDisLikes = videoI.videoDisLikes
            videoComments = videoI.videoComments
            videoViews = videoI.videoViews

            # 作者方面信息
            videoUserId = videoI.videoUserId
            userAvatar = user.objects.get(userId=int(videoUserId)).userAvatar
            # 枚举信息
            videoLocation = videoI.videoLocation
            videoGoal = videoI.videoGoal
            videoMusucle = videoI.videoMusucle
            videoDifficulty = videoI.videoDifficulty
            videoTool = videoI.videoTool

            # 评论列表
            dataList = []
            try:
                for cm in comment.objects.filter(cmVId=mId).all():
                    text = cm.cmText
                    time1 = str(cm.cmTime)
                    likeCount = cm.cmLikeCount
                    disLikeCount = cm.cmDisLikeCount
                    cmId = cm.cmId
                    cmUserID = cm.cmUserId
                    UserI = user.objects.filter(userId=int(cmUserID))[0]
                    #print(cmUserID,str(UserI))
                    cmUserAvatar = UserI.userAvatar
                    cmUserAlias = UserI.userAlias

                    data1 = {
                        'cmUserId':cmUserID,
                        'cmUserAvatar':cmUserAvatar,
                        'cmUserAlias':cmUserAlias,
                        'cmId': cmId,
                        'text': text,
                        'time': time1,
                        'likeCount': likeCount,
                        'disLikeCount': disLikeCount,


                    }
                    dataList.append(data1)
            except Exception as e:
                print(str(e))

            data1 = {
                'commentList': dataList,
                'videoUserId':videoUserId,
                'userAvatar':userAvatar,
                'voiceCover': videoCover,
                'Voice':videoSrc,
                'Info':videoInfo,
                'Title':videoTitle,

                'videoLikes':videoLikes,
                'videoDisLikes':videoDisLikes,
                'videoComments':videoComments,
                'videoViews':videoViews,

                'videoTime':str(videoTime),
                'videoDuration':videoDuration,

                'videoMusucle':videoMusucle,
                'videoGoal':videoGoal,
                'videoLocation':videoLocation,
                'videoDifficulty':videoDifficulty,
                'videoTool':videoTool,
            }
            return JsonResponse(data1)
        except Exception as e:
            print(str(e)+'fffff')
            try:
                #print('p22')
                musucle = int(request.POST.get('musucle'))
                mslist = []
                msList = video.objects.filter(videoMusucle=musucle).order_by('videoLikes')


                for videoI in msList:
                    videoTitle = videoI.videoTitle
                    videoInfo = videoI.videoInfo
                    videoTime = videoI.videoTime
                    videoCover = videoI.videoCover
                    # 时长可以通过 上传video的时候就获取到了 存数据库就好
                    videoDuration = videoI.videoDuration

                    # like dislike comment Counts!
                    videoLikes = videoI.videoLikes
                    videoDisLikes = videoI.videoDisLikes
                    videoComments = videoI.videoComments
                    videoViews = videoI.videoViews

                    # 作者方面信息
                    videoUserId = videoI.videoUserId
                    userAvatar = user.objects.get(userId=int(videoUserId)).userAvatar
                    # 枚举信息
                    videoLocation = videoI.videoLocation
                    videoGoal = videoI.videoGoal
                    videoMusucle = videoI.videoMusucle
                    videoDifficulty = videoI.videoDifficulty
                    videoTool = videoI.videoTool

                    data1 = {
                        'videoUserId': videoUserId,
                        'userAvatar': userAvatar,

                        'VoiceCover': videoCover,
                        'Info': videoInfo,
                        'Title': videoTitle,

                        'videoLikes': videoLikes,
                        'videoDisLikes': videoDisLikes,
                        'videoComments': videoComments,
                        'videoViews': videoViews,

                        'videoTime': str(videoTime),
                        'videoDuration': videoDuration,

                        'videoMusucle': videoMusucle,
                        'videoGoal': videoGoal,
                        'videoLocation': videoLocation,
                        'videoDifficulty': videoDifficulty,
                        'videoTool': videoTool,
                    }
                    mslist.append(data1)
                return HttpResponse(json.dumps(mslist, ensure_ascii=False))
            except Exception as e:
                print('坐标和videoID都没有！' + str(e))
                return render(request, '404.html')
    else:
        return render(request, 'edot_getVideo.html')


def storing(request,cmd):
    if cmd==1:
        cmdstr = 'avatar'
    elif(cmd==2):
        cmdstr = 'video'
    else:
        cmdstr = 'cover'
    #print('p1')
    fileI = request.FILES.get(cmdstr, None)
    #print('p2')
    fileNameI = fileI.name.split('.')
    if not fileI:
        return -1
    filename = fileNameI[0] + str(get_unique_str(6)) + '.' + fileNameI[1]
    #print('p3')
    try:
        storing = open(os.path.join('media/Edot/',cmdstr,filename), 'wb+')
    except Exception as e:
        print(e)
        storing=''
        return -1
        #print(os.path.join('media/',cmdstr,filename))
    for chunk in fileI.chunks():
        storing.write(chunk)
    storing.close()
    print(filename + 'storing oK')
    return filename


ListStringData=[
  ['健身房','家里','运动场'],
  ['杠铃','跑步机','瑜伽垫','','','',''],
  ['练腹肌','练胸肌','瘦腿','练手臂'],
  [
    '斜方肌上中部','三角肌前束','肱二头肌','前臂肌','胸肌','腹肌','股外侧肌','小腿三头肌',
    '斜方肌下部','三角肌中后束','肱三头肌','前臂肌','背肌','腰肌','股外侧肌','小腿三头肌',
    '臀中肌','臀大肌',
  ],
  ['简单','一般','较难','困难','挑战','极限'],
]


#
def createUserVideo(request):
    # t = int(time())%10000
    dictJson = {}
    videoI = video()

    if request.method == "POST":
        try:
            avatar = storing(request, 1)
            userI = user.create(userAvatar=avatar)
            userI.save()
            videoI.videoUserId = userI.userId
            videoI.userAvatar = avatar
            videoI.videoCover = storing(request, 3)
            videoI.videoSrc = storing(request, 2)
            # videoDuration ????
            musucle = int(request.POST.get('musucle'))
            videoI.videoMusucle = musucle
            # videoI.videoMusucle = int(random.randrange(0,17))
            videoI.videoTitle = ListStringData[3][videoI.videoMusucle]+'——from'+str(userI.userAlias)
            videoI.videoInfo = videoInfoList[int(random.randrange(0,10))]
            # videoDuration ????
            videoI.videoGoal = int(random.randrange(0,3))
            videoI.videoTool = int(random.randrange(0,3))
            videoI.videoDifficulty = int(random.randrange(0, 3))
            videoI.videoLocation = int(random.randrange(0, 3))
            videoI.save()

            videoI = video.objects.last()
            times = int(random.randrange(3, 10))
            for i in range(1,times+1):
                commentI = comment()
                commentI.cmText = CommentList[int(random.randrange(1,10))]
                commentI.cmUserId = str(user.objects.all()[random.randrange(0,int( user.objects.count()))].userId)
                commentI.cmVId = str(videoI.videoId)

                commentI.save()

            videoI.videoComments = times
            videoI.save()
            print(str(video.objects.last().videoId)+' added comments ')
            return render(request, 'edot_uploadUserResult.html', context={
            "user": userI,
            "video": videoI,

        })
        except AttributeError as e:
            print(e)
            dictJson['code'] = -3
            return JsonResponse(dictJson)
        except Exception as e:
            print(e)
            dictJson['code'] = -4
            return JsonResponse(dictJson)
    else:
        return render(request, 'edot_uploadUser.html')


# 从已有用户中 抽取出来随机给现有的视频点赞 点踩 评论
def createLikeVideo(request):
    ## 给video点赞 1~20
    try:
        flag = int(random.randrange(0,2))
        allVideo = video.objects.all()
        for c in allVideo:
            videoId = c.videoId
            times = random.randrange(1,10)
            for i in range(1, times):
                if flag == 0:
                    likeI = like()
                    likeI.likeVId = str(videoId)
                    likeI.likeUserId = getRandomLikeUser(1, str(videoId))
                    likeI.save()

                elif flag == 1:
                    DislikeI = Dislike()
                    DislikeI.disLikeVId = str(videoId)
                    DislikeI.disLikeUserId = getRandomDisLikeUser(1, str(videoId))
                    DislikeI.save()

            if flag == 0:

                videoII = video.objects.filter(videoId=videoId)[0]
                likes = videoII.videoLikes
                videoII.videoLikes = likes + times
                videoII.save()
            elif flag == 1:
                videoII = video.objects.filter(videoId=videoId)[0]
                dislikes = videoII.videoDisLikes
                videoII.videoDisLikes = dislikes + times
                videoII.save()

    except Exception as e:
        print(e)

        ## 给comment点赞 1~20

    return HttpResponse("good")

def createLikeComment(request):
    try:
        flag = int(random.randrange(0,2))

        for c in comment.objects.all():
            cmId = c.cmId
            times = random.randrange(1, 10)
            for i in range(1, times):
                if flag == 0:
                    likeI = like()
                    likeI.likeCmId = str(cmId)
                    likeI.likeUserId = getRandomLikeUser(2, str(cmId))
                    likeI.save()

                elif flag == 1:
                    DislikeI = Dislike()
                    DislikeI.disLikeCmId = str(cmId)
                    DislikeI.disLikeUserId = getRandomDisLikeUser(2, str(cmId))
                    DislikeI.save()

            if flag == 0:
                commentII = comment.objects.filter(cmId=cmId)[0]
                likes = commentII.cmLikeCount
                commentII.cmLikeCount = likes + times
                commentII.save()
            elif flag == 1:
                commentII = comment.objects.filter(cmId=cmId)[0]
                likes = commentII.cmDisLikeCount
                commentII.cmDisLikeCount = likes + times
                commentII.save()
    except Exception as e:
        print(e)
    return HttpResponse("good")

def createSuper(request):
    pass

