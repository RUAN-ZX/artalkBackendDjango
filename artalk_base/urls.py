#-*- utf-8 -*-
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "files"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

urlpatterns = [
    # 创建
    re_path('create/$',views.createUM,name='createUM'),

    re_path('createComment/$',views.createComment,name='createComment'),
    re_path('createUser/$',views.createUser,name='createUser'),
    re_path('createMessage/$',views.createMessage,name='createMessage'),
    # 删除 取消类
    re_path('deleteMessage/$',views.deleteMessage,name="deleteMessage"),
    re_path('deleteComment/$',views.deleteComment,name="deleteComment"),
    # 获取信息：
    re_path('getMessage/$',views.getMessage,name='getMessage'),
    re_path('getUser/$',views.getUser,name="getUser"),


    # 留言点赞点踩etc
    re_path('toggleMsLike/$',views.toggleMsLike,name='createMsLike'),
    re_path('toggleMsDisLike/$',views.toggleMsDisLike,name='createMsDisLike'),
    # re_path('deleteMsDisLike/$',views.deleteMsDisLike,name='deleteMsDisLike'),
    # re_path('msLikeStatus/$',views.msLikeStatus,name='msLikeStatus'),

    # 评论点赞点踩etc
    re_path('toggleCmLike/$',views.toggleCmLike,name='createCmLike'),
    # re_path('deleteCmLike/$',views.deleteCmLike,name='deleteCmLike'),
    re_path('toggleCmDisLike/$',views.toggleCmDisLike,name='createCmDisLike'),

    # re_path('deleteCmDisLike/$',views.deleteCmDisLike,name='deleteCmDisLike'),
    #
    # re_path('cmLikeStatus/$',views.cmLikeStatus,name='cmLikeStatus'),


]
app_name='artalk_base'
