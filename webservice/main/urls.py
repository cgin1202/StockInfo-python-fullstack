# main 서브앱의 urls
# 서브앱의 urls는 같은 위치의 view.py의 함수로 연결 담당 (path)
# 같은 위치의 view.py를 식별 못하면 import

from django.contrib import admin
from django.urls import path, include
from . import views                         # 같은 위치의 views 참조


urlpatterns = [
    path('',views.index, name='index'),   
    path('index',views.index, name='index'), 
]
