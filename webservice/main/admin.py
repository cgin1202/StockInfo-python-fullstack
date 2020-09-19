from django.contrib import admin

# 관리를 위한 DB 등록
from .models import US_Stock

admin.site.register(US_Stock)

# Register your models here.
