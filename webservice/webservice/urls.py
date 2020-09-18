
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/',include('main.urls')),          # 서브앱.urls 추가
]
