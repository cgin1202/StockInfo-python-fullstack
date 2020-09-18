from django.shortcuts import render

from yahoo_finance import Share         # Yahoo Finance API
from django.http import HttpResponse
from django.template import loader
#import json

# Create your views here.


def index(reqeust):
    template=loader.get_template('main/index.html')

    samsung = Share('005930.KS') # 객체 초기화
    print(samsung)

    return HttpResponse(template.render(contenxt, request))

