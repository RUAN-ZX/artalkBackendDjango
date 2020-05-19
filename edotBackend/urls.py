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
re_path('createUserVideo/$',views.createUserVideo,name='createUserVideo'),
    # 创建


]
app_name='edotBackend'
