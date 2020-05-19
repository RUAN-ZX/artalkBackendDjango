import os
import random
from time import time
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import uuid,hashlib
from .models import message, user,comment,like,Dislike
import json

commentExampleList = [
    "一年之计，莫如树谷；十年之计，莫如树木；百年之计，莫如树人。",
    "你站在阴影里，却说太阳对你不公平。",
    "古之立大事者，不惟有超世之才，亦必有坚忍不拔之志。",
    "骐骥一跃，不能十步；驽马十驾，功在不舍。",
    "这个世界上，取得成功的人是那些努力寻找他们想要机会的人，如果找不到机会，他们就去创造机会。",
    "荷叶生时春恨生，荷叶枯时秋恨成。深知身在情长在，怅望江头江水声。",
    "冬天把旧叶子揉掉了，你要听新故事吗？静静的乌江睁着眼睛，笑着对你说：总有回家的人，总有离岸的船。",
    "我们很难讨论存活得失之间的相对价值，却也始终为活着的那份存在甚至于永恒的精神而感动终身。",
    "如果，蓝天是一本无字天书，云必是无字的注脚，而你的踏雪乌骓则翻译云的语言于驰道。",
    "你想，这乌江之所以雄伟，在于她以海域般的雅量回合每一支氏族颠沛流离的故事合撰成一部大传奇，你从中阅读别人带血的篇章，也看到你项氏祖先所佔、染血的那一行。",
    "或许行年渐晚，深知在这个你曾经称雄的世间，能完整实践理想中的美，愈来愈不可得，触目所见多是无法拼凑完全的碎片,和着垓下的楚歌——故乡的歌。",
]
messageExampleList = [
    "路漫漫其修远兮，吾将上下而求索。",
    "你所谓的岁月静好，是因为有人在负重前行",
    "今生不悔入华夏，来世还愿种花家。",
    "那年乱世如麻，愿你们来世拥有锦绣年华",
    "亲们 ，大国梦的实现 ，不纯靠嘴。",
    "知不足，然后能自反也；知困，然后能自强也。",
    "为人性僻耽佳句，语不惊人死不休",
    "博观而约取，厚积而薄发。",
    "不战而屈人之兵，善之善者也。",
    "以铜为镜，可以正衣冠；以古为镜，可以知兴替；以人为镜，可以明得失。",
    "革命尚未成功，同志仍须努力。",
]

def get_unique_str():
    uuid_str = str(uuid.uuid4())
    md5 = hashlib.md5()
    md5.update(uuid_str.encode('utf-8'))
    return md5.hexdigest()


def ValidationPk(modelI,id):
    # 小心get的问题！
    #if model.objects==models.manager.QuerySet:
        if modelI.objects.filter(pk=id):
            return 1
        else:
            return 0


# 还要获得评论 点赞等
# def getCommentDict(messageId):
#     commentDict = {}
#     try:
#         commentI = comment.objects.filter(cmMsId=messageId)
#         if not commentI:
#             return 0
#         for i in commentI:
#             commentDict[str(i.cmUserId)]=str(i.cmText)
#         return commentDict
#     except Exception as e:
#         return 0


def transform(a):
    if(a==True):
        return 3
    elif(a==False):
        return 2
    else:
        return 1



def getMessage(request):
    if request.method == "POST":
        try:
            mId = request.POST.get('mId')
            mId = int(mId)
            messageI = message.objects.get(msId=mId)
            Voice = messageI.msVoice
            Text = messageI.msText
            # 再想能不能定期检查更新一波就简单了
            LikeCount = messageI.msLikeCount
            DisLikeCount = messageI.msDisLikeCount

            # 获取留言的评论列表
            dataList = []
            try:
                for cm in comment.objects.filter(cmMsId=mId).all():
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
                print('11'+str(e))
            commentCount = messageI.msCmCount
            mstime = messageI.msTime
            msUserId = messageI.msUserID
            data1 = {
                'commentList': dataList,
                'msUserId':msUserId,
                'Voice':Voice,
                'Text':Text,
                'likeCount':LikeCount,
                'DislikeCount':DisLikeCount,
                'commentCount':commentCount,
                'time':str(mstime),
            }
            return JsonResponse(data1)
        except Exception as e:
            print(str(e)+'fffff')
            try:
                #print('p22')
                Cx = request.POST.get('cx')
                print(type(Cx))
                Cx = int(Cx)
                Cy = request.POST.get('cy')
                #print(type(Cy))
                Cy = int(Cy)
                offset = 50
                data1 = {}
                conditionQ = Q(msCx__lt=Cx + offset) & Q(msCx__gt=Cx - offset) & Q(msCy__lt=Cy + offset) & Q(msCy__gt=Cy - offset)
                msList = message.objects.filter(conditionQ).order_by('msCx').order_by('msCy')
                mslist = []

                for ms in msList:
                    if bool(ms.msVoice)&bool(ms.msText):
                        mstype = 3
                    elif ms.msVoice:
                        mstype = 2
                    else:
                        mstype = 1
                    uid = ms.msUserID
                    avatar = user.objects.filter(userId=uid)[0].userAvatar
                    LikeCount = ms.msLikeCount
                    DisLikeCount = ms.msDisLikeCount
                    commentCount = ms.msCmCount
                    mstime = ms.msTime
                    data1 = {
                        'msId':str(ms.msId),
                        'userId': uid,
                        'likeCount':LikeCount,
                        'DislikeCount':DisLikeCount,
                        'commentCount': commentCount,
                        'mstype':mstype,
                        'time':str(mstime),
                        'avatar':avatar,
                    }
                    mslist.append(data1)
                return HttpResponse(json.dumps(mslist, ensure_ascii=False))
            except Exception as e:
                print('坐标和messageID都没有！' + str(e))
                return render(request, '404.html')
    else:
        return render(request, 'artalk_getMessage.html')



def storing(t,request,cmd):
    if cmd==1:
        cmdstr = 'Avatar'
    else:
        cmdstr = 'Voice'
    #print('p1')
    fileI = request.FILES.get(cmdstr, None)
    #print('p2')
    fileNameI = fileI.name.split('.')
    if not fileI:
        return -1
    filename = fileNameI[0] + str(t) + '.' + fileNameI[1]
    #print('p3')
    try:
        storing = open(os.path.join('media/',cmdstr,filename), 'wb+')
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


# ok
def createUser(request):
    t = int(time())
    dictJson = {}
    userI = user()
    if request.method == "POST":
        try:
            userI.userAlias = request.POST.get('alias')
            userI.userGender = request.POST.get('gender')
            userI.userPhone = request.POST.get('phone')
            userI.userPwd = request.POST.get('password')
            if user.objects.filter(userAlias=userI.userAlias):
                dictJson['code'] = -1
                return JsonResponse(dictJson)
            if user.objects.filter(userPhone=userI.userPhone):
                dictJson['code'] = -2
                return JsonResponse(dictJson)
            print('33')
            avatar = storing(t, request, 1)
            # if not avatar:
            #     dictJson['code'] = -3
            #     return JsonResponse(dictJson)
            userI.userAvatar = avatar
            userI.save()
            return render(request, 'artalk_uploadUserResult.html', context={"user": userI})
        except AttributeError:
            dictJson['code'] = -3
            return JsonResponse(dictJson)
        except Exception as e:
            print(e)
            dictJson['code'] = -4
            return JsonResponse(dictJson)
    else:
        return render(request, 'artalk_uploadUser.html')

# ok
def createMessage(request):
    t = int(time())
    dictJson = {}
    messageI = message()
    if request.method == "POST":
        try:
            Text = str(request.POST.get('text'))
            cx = int(request.POST.get('cx'))
            cy = int(request.POST.get('cy'))
            userId = int(request.POST.get('userId'))
            if not ValidationPk(user, userId):
                dictJson['code'] = -1
                return JsonResponse(dictJson)
        except Exception as e:
            print(e)
            dictJson['code'] = -3
            return JsonResponse(dictJson)
        #
        try:


            messageI.msUserID = userId
            messageI.msText = Text
            messageI.msCx = float(cx)
            messageI.msCy = float(cy)
            voice = storing(t, request, 2)
            messageI.msVoice = voice
            messageI.save()
            msId = str(message.objects.last().msId)
            data1 = {
                'msId':msId,
            }
            return JsonResponse(data1)
        # 没音频的时候
        except AttributeError:
            if not request.POST.get('text'):
                dictJson['code'] = -2
                return JsonResponse(dictJson)
            messageI.msVoice = ''
            messageI.save()
            msId = str(message.objects.last().msId)
            data2 = {
                'msId': msId,
            }
            return JsonResponse(data2)
        except Exception as e:
            print(e)
            dictJson['code'] = -4
            return JsonResponse(dictJson)
    else:
        return render(request, 'artalk_uploadMessage.html')


# ok
def createComment(request):
    returnDict = {}

    if request.method == 'POST':
        try:
            uId = request.POST.get('userId')
            mId = request.POST.get('messageId')
            text = request.POST.get('text')
            uV = ValidationPk(user,uId)
            mV = ValidationPk(message,mId)
            if (uV==0&mV==0):
                returnDict['code'] = -4
                return JsonResponse(returnDict)
            elif not uV:
                returnDict['code'] = -1
                return JsonResponse(returnDict)
            elif not mV:
                returnDict['code'] = -2
                return JsonResponse(returnDict)

            #user_id_invalided = 'setComment user 不存在！'
            #ms_id_invalided = "setComment message 不存在！"

            else:

                commentI = comment()
                commentI.cmMsId = str(mId)
                commentI.cmUserId = str(uId)
                commentI.cmText = str(text)
                commentI.save()

                cmCountPlus = message.objects.get(msId=int(mId))
                cmCountPlus.msCmCount = cmCountPlus.msCmCount+1
                cmCountPlus.save()
                returnDict['cmId'] = comment.objects.last().cmId
                return JsonResponse(returnDict)
        except Exception as e:
            print(e)
            returnDict['code'] = -3
            return JsonResponse(returnDict)
            # 这里到达不了 后面再看

    else:
         return render(request,'artalk_setComment.html')
        # returnDict['code'] = -5
        # return JsonResponse(returnDict)

# 和过去的点赞是否重复！！
# 不能一条评论点两个赞！
# 评论那边 倒是无所谓！
# ok

# ok



def getRandomDisLikeUser(code,id):

    # 假设目前有30用户！
    userI = user.objects.all()[random.randrange(0, 100)].userId
    # 当code=1 是给message点赞
    if code:
        # CmId 为空 那么msId就有值了
        if not bool(
                Dislike.objects.filter(Q(disLikeUserId=userI)&Q(disLikeMsId=id))&like.objects.filter(Q(likeUserId=userI)&Q(likeMsId=id))):
            return userI
        else:
            return getRandomDisLikeUser(code,id)
    # 是为了comment点赞：
    else:
        if not Dislike.objects.filter(Q(disLikeCmId=id)&Q(disLikeUserId=userI))&like.objects.filter(Q(likeUserId=userI)&Q(likeCmId=id)):
            return userI
        else:
            return getRandomDisLikeUser(code,id)


def getRandomLikeUser(code,id):
    # 假设目前有30用户！
    userI = user.objects.all()[random.randrange(0, 100)].userId
    print('11')
    # 当code=1 是给message点赞
    if code:
        # CmId 为空 那么msId就有值了
        if not bool(like.objects.filter(Q(likeMsId=id) & Q(likeUserId=userI)))&bool(Dislike.objects.filter(Q(disLikeMsId=id) & Q(disLikeUserId=userI))):
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



def createUM(request):
    t = int(time())
    if request.method == "POST":
        avatar = storing(t,request,1)
        if not avatar:
            return HttpResponse('No file!!!')
        userI = user().create(t % 100,avatar)
        userI.save()
        voice = storing(t, request, 2)
        messageI = message()
        #messageI.msLikeCount = 0
        messageI.msVoice = voice
        messageI.msCx = t%50
        messageI.msCy = 100 - t%50
        messageI.msText = messageExampleList[t % 10]
        messageI.msUserID = str(user.objects.last().userId)
        messageI.save()

        # 一个message3个评论
        # 3个评论 每个评论一个人 一个人可以发很多评论

        # 刷赞
        try:
            flag = int(time())
            msId1 = message.objects.last().msId
            for i in range(1,4):
                if flag%2==0:
                    likeI = like()
                    likeI.likeMsId = str(msId1)
                    likeI.likeUserId = getRandomLikeUser(1,str(msId1))
                    likeI.save()

                elif flag%2==1:
                    DislikeI = Dislike()
                    DislikeI.disLikeMsId = str(msId1)
                    DislikeI.disLikeUserId = getRandomDisLikeUser(1,str(msId1))
                    DislikeI.save()

            if flag%2==0:
                message.objects.last().msLikeCount = 3
            elif flag%2==1:
                message.objects.last().msDisLikeCount = 3
        except Exception as e:
            print(e)

        # for i in range(1,4):
        #     LikeI = like()
        #     commentI = comment()
        #     commentI.cmMsId = str(message.objects.last().msId)
        #
        #     commentI.cmText = commentExampleList[random.randrange(0, 10)]
        #
        #     commentI.cmUserId = str(user.objects.all()[random.randrange(0,10)].userId)
        #
        return render(
            request,
            'artalk_uploadUMResult.html',
            context={
                "user": userI,
                "message":messageI,

            })
    else:
        return render(request, 'artalk_uploadUM.html')





def toggleMsLike(request):
    returnDict = {}
    if request.method == 'POST':
        try:
            uId = request.POST.get('userId')
            mId = request.POST.get('msId')
            uV = ValidationPk(user, uId)
            mV = ValidationPk(message, mId)
            # 检测留言重复点赞
            umV = like.objects.filter(Q(likeMsId=mId)&Q(likeUserId=uId))
            DislikeI = Dislike.objects.filter(Q(disLikeMsId=mId) & Q(disLikeUserId=uId))
            if not uV|mV:
                returnDict['code'] = -5
                return JsonResponse(returnDict)
            if not uV:
                returnDict['code'] = -2
                return JsonResponse(returnDict)
            if not mV:
                returnDict['code'] = -3
                return JsonResponse(returnDict)

            if umV:
                umV.delete()
                msCountPlus = message.objects.get(msId=int(mId))
                msCountPlus.msLikeCount = msCountPlus.msLikeCount - 1
                msCountPlus.save()
            else:
                if DislikeI:
                    returnDict['code'] = -1
                    return JsonResponse(returnDict)
                else:
                    LikeI = like()
                    LikeI.likeMsId = str(mId)
                    LikeI.likeUserId = str(uId)
                    LikeI.save()

                    msCountPlus = message.objects.get(msId=int(mId))
                    msCountPlus.msLikeCount = msCountPlus.msLikeCount + 1
                    msCountPlus.save()

            LikeI = like.objects.filter(Q(likeMsId=mId) & Q(likeUserId=uId))
            if DislikeI:
                returnDict['code'] = 2
                return JsonResponse(returnDict)
            if LikeI:
                returnDict['code'] = 1
                return JsonResponse(returnDict)
            if not bool(DislikeI) & bool(LikeI):
                returnDict['code'] = 3
            return JsonResponse(returnDict)
        except Exception as e:
            # 缺参数
            returnDict['code'] = -4
            return JsonResponse(returnDict)

    else:
        return render(request, 'artalk_createMsLike.html')
        #returnDict['code'] = -6
        #eturn JsonResponse(returnDict)
## ok
def toggleMsDisLike(request):
    returnDict = {}
    if request.method == 'POST':
        try:
            uId = request.POST.get('userId')
            mId = request.POST.get('msId')
            uV = ValidationPk(user, uId)
            mV = ValidationPk(message, mId)
            # 检测留言重复点赞
            umV = Dislike.objects.filter(Q(disLikeMsId=mId) & Q(disLikeUserId=uId))
            LikeI = like.objects.filter(Q(likeMsId=mId) & Q(likeUserId=uId))

            if not uV | mV:
                returnDict['code'] = -5
                return JsonResponse(returnDict)
            if not uV:
                returnDict['code'] = -2
                return JsonResponse(returnDict)
            if not mV:
                returnDict['code'] = -3
                return JsonResponse(returnDict)
            # 如果已经存在 那就删除
            if umV:
                umV.delete()
                msCountPlus = message.objects.get(msId=int(mId))
                msCountPlus.msDisLikeCount = msCountPlus.msDisLikeCount -1
                msCountPlus.save()
            # 不能存在就增加
            else:
                if LikeI:
                    returnDict['code'] = -1
                    return JsonResponse(returnDict)
                else:
                    LikeI = Dislike()
                    LikeI.disLikeMsId = str(mId)
                    LikeI.disLikeUserId = str(uId)
                    LikeI.save()

                    msCountPlus = message.objects.get(msId=int(mId))
                    msCountPlus.msDisLikeCount = msCountPlus.msDisLikeCount + 1
                    msCountPlus.save()


            DislikeI = Dislike.objects.filter(Q(disLikeMsId=mId) & Q(disLikeUserId=uId))
            if DislikeI:
                returnDict['code'] = 2
                return JsonResponse(returnDict)
            if LikeI:
                returnDict['code'] = 1
                return JsonResponse(returnDict)
            if not (bool(DislikeI) | bool(LikeI)):
                returnDict['code'] = 3
            return JsonResponse(returnDict)
        except Exception as e:
            # 缺参数
            returnDict['code'] = -4
            return JsonResponse(returnDict)

    else:
        return render(request, 'artalk_createMsDisLike.html')


# ok
def toggleCmDisLike(request):
    returnDict = {}
    if request.method == 'POST':
        try:
            uId = request.POST.get('userId')
            mId = request.POST.get('cmId')
            uV = ValidationPk(user, uId)
            mV = ValidationPk(comment, mId)
            # 检测留言重复点赞
            umV = Dislike.objects.filter(Q(disLikeCmId=mId) & Q(disLikeUserId=uId))
            LikeI = like.objects.filter(Q(likeCmId=mId) & Q(likeUserId=uId))
            if not uV | mV:
                returnDict['code'] = -5
                return JsonResponse(returnDict)
            if not uV:
                returnDict['code'] = -2
                return JsonResponse(returnDict)
            if not mV:
                returnDict['code'] = -3
                return JsonResponse(returnDict)

            if umV:
                umV.delete()
                cmCountPlus = comment.objects.get(cmId=int(mId))
                cmCountPlus.cmDisLikeCount = cmCountPlus.cmDisLikeCount - 1
                cmCountPlus.save()
            else:
                if LikeI:
                    returnDict['code'] = -1
                    return JsonResponse(returnDict)
                else:
                    LikeI = Dislike()
                    LikeI.disLikeCmId = str(mId)
                    LikeI.disLikeUserId = str(uId)
                    LikeI.save()

                    cmCountPlus = comment.objects.get(cmId=int(mId))
                    cmCountPlus.cmDisLikeCount = cmCountPlus.cmDisLikeCount + 1
                    cmCountPlus.save()

            DislikeI = Dislike.objects.filter(Q(disLikeCmId=mId) & Q(disLikeUserId=uId))

            if DislikeI:
                returnDict['code'] = 2
                return JsonResponse(returnDict)
            if LikeI:
                returnDict['code'] = 1
                return JsonResponse(returnDict)
            if not bool(DislikeI) & bool(LikeI):
                returnDict['code'] = 3
            return JsonResponse(returnDict)

        except Exception as e:
            # 缺参数
            returnDict['code'] = -4
            return JsonResponse(returnDict)

    else:
        return render(request, 'artalk_createCmDisLike.html')

def toggleCmLike(request):
    returnDict = {}
    if request.method == 'POST':
        try:
            uId = request.POST.get('userId')
            cId = request.POST.get('cmId')
            uV = ValidationPk(user, uId)
            cV = ValidationPk(comment, cId)
            # 检测留言重复点赞
            ucV = like.objects.filter(Q(likeCmId=cId)&Q(likeUserId=uId))
            DislikeI = Dislike.objects.filter(Q(disLikeCmId=cId) & Q(disLikeUserId=uId))
            if not uV|cV:
                returnDict['code'] = -5
                return JsonResponse(returnDict)
            if not uV:
                returnDict['code'] = -2
                return JsonResponse(returnDict)
            if not cV:
                returnDict['code'] = -3
                return JsonResponse(returnDict)
            print('11')
            if ucV:
                ucV.delete()
                cmCountPlus = comment.objects.get(cmId=int(cId))
                cmCountPlus.cmLikeCount = cmCountPlus.cmLikeCount - 1
                cmCountPlus.save()
            else:
                if DislikeI:
                    returnDict['code'] = -1
                    return JsonResponse(returnDict)
                else:
                    LikeI = like()
                    LikeI.likeCmId = str(cId)
                    LikeI.likeUserId = str(uId)
                    LikeI.save()

                    cmCountPlus = comment.objects.get(cmId=int(cId))
                    cmCountPlus.cmLikeCount = cmCountPlus.cmLikeCount + 1
                    cmCountPlus.save()


            LikeI = like.objects.filter(Q(likeCmId=cId) & Q(likeUserId=uId))
            if DislikeI:
                returnDict['code'] = 2
                return JsonResponse(returnDict)
            if LikeI:
                returnDict['code'] = 1
                return JsonResponse(returnDict)
            if not bool(DislikeI) & bool(LikeI):
                returnDict['code'] = 3
            return JsonResponse(returnDict)

        except Exception as e:
            print('33'+str(e))
            # 缺参数
            returnDict['code'] = -4
            return JsonResponse(returnDict)

    else:
        return render(request,'artalk_createCmLike.html')
        #returnDict['code'] = -6
        #return JsonResponse(returnDict)




def deleteMessage(request):
    returnDict = {}
    if request.method == 'POST':
        try:
            mId = request.POST.get('msId')
            mV = ValidationPk(message, mId)

            if not mV:
                returnDict['code'] = - 1
                return JsonResponse(returnDict)

            message.objects.filter(msId=int(mId)).delete()
            comment.objects.filter(cmMsId=int(mId)).delete()
            like.objects.filter(likeMsId=int(mId)).delete()

            Dislike.objects.filter(disLikeMsId=int(mId)).delete()
            returnDict['code'] = 0
            return JsonResponse(returnDict)
        except Exception as e:
            # 缺参数
            returnDict['code'] = -2
            return JsonResponse(returnDict)

    else:
        return render(request, 'artalk_deleteMessage.html')

# ok
def getUser(request):
    returnDict = {}
    if request.method == 'POST':
        try:
            mId = request.POST.get('userId')
            mV = ValidationPk(user, mId)

            if not mV:
                returnDict['code'] = - 1
                return JsonResponse(returnDict)

            u = user.objects.filter(userId=int(mId))[0]
            dataU = {
                'alias':str(u.userAlias),
                'phone':u.userPhone,
                'gender':str(u.userGender),
                'avatar':u.userAvatar,

            }
            return JsonResponse(dataU)
        except Exception as e:
            print(e)
            returnDict['code'] = -2
            return JsonResponse(returnDict)

    else:
        return render(request, 'artalk_getUser.html')


def deleteComment(request):
    returnDict = {}
    if request.method == 'POST':
        try:
            mId = request.POST.get('cmId')
            mV = ValidationPk(comment, mId)

            if not mV:
                returnDict['code'] = - 1
                return JsonResponse(returnDict)

            comment.objects.filter(cmId=int(mId)).delete()
            like.objects.filter(likeCmId=int(mId)).delete()

            Dislike.objects.filter(disLikeCmId=int(mId)).delete()
            returnDict['code'] = 0
            return JsonResponse(returnDict)
        except Exception as e:
            # 缺参数
            returnDict['code'] = -2
            return JsonResponse(returnDict)

    else:
        return render(request, 'artalk_deleteComment.html')
# 63 95
