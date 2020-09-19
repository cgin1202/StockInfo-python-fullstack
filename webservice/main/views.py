from django.shortcuts import render            # 기본 반환값 (템플릿 지정 함수)
from yahoo_finance import Share                 # Yahoo Finance API
from django.template import loader
from main.models import US_Stock
import json
from django.http import HttpResponse
from django.template import loader
from django.db.models import Avg
from django.db.models import Sum
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.db.models import F
import math
#from django.db.models import Func

# Create your views here.

#class Round(Func):
#       function = 'ROUND'
#       template='%(function)s(%(expressions)s, 2)'

def index(request):
    template=loader.get_template('main/index.html')

    queryset=US_Stock.objects.values(
        'symbol'
    ).annotate(
        max_profit=Max(F('highvalue')-F('lowvalue')),
        min_profit=Min(F('highvalue')-F('lowvalue')),
        avg_value=Avg((F('closevalue')+F('openvalue'))/2),
        avg_volume=Avg('volumevalue')
    ).order_by(
        'symbol'
    )

    # 소수점 처리
    for i in queryset:
        i['max_profit']=round(i['max_profit'], 2)
        i['min_profit']=round(i['min_profit'], 2)
        i['avg_volume']=round(i['avg_volume'], 2)
        i['avg_value']=round(i['avg_value'], 2)
    context={
        'stocks' : queryset,
    }
    return HttpResponse(template.render(context, request))

