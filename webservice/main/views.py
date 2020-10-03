###############################################################
# Python Django ORM에 해당하는 Model import

from main.models import US_Stock

###############################################################
# 템플릿 지정 함수 및 통신을 위한 모듈 import

from django.shortcuts import render            
from django.template import loader
from django.http import HttpResponse
import json

###############################################################
# Python Django ORM의 Object에 대해서 Aggregate, Annotate 연산을 수행하기 위한 import

from django.db.models import Avg
from django.db.models import Sum
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.db.models import F

###############################################################
# 우선순위 큐 import

from queue import PriorityQueue

###############################################################
# datetime to integer 함수

def to_integer(dt_time):
    return 10000*dt_time.year+100*dt_time.month+dt_time.day




###############################################################
# 슬라이딩 윈도우 알고리즘을 사용하여 minvalue를 수정하면서 maxprofit 구하기
# 시간복잡도 = O(N)

def max_profit2(date_list, highvalue_list, lowvalue_list):
  n=len(highvalue_list)
  buy_date=date_list[0]               # Profit 최대로 낼 수 있는 구매한 날
  sell_date=date_list[0]                # Profit 최대로 낼 수 있는 판매한 날
  getResult=[]
  maxProfit=0
  minPrice=lowvalue_list[0]
  
  for i in range(1,n):
    profit=highvalue_list[i]-minPrice
    if(profit>maxProfit):
      maxProfit=profit
      sell_data=date_list[i]
    if(lowvalue_list[i]<minPrice):
      minPrice=lowvalue_list[i]
      buy_date=date_list[i]
    
  getResult.append(maxProfit)
  getResult.append(buy_date)
  getResult.append(sell_date)

  return getResult


###############################################################
# 현재 있는 low_value를 기준으로 가장 크게 profit을 얻을 수 있는 날을 확인하고, Max를 취하여 결과값 도출
# 시간복잡도 N*N = O(N^2)

def getMaxProfit(date_list, highvalue_list, lowvalue_list):

    getResult=[]
    
    buy_date=0               # Profit 최대로 낼 수 있는 구매한 날
    sell_date=0                # Profit 최대로 낼 수 있는 판매한 날
    size=len(date_list)
    maxProfit=0               # Profit 최대값 저장 변수

    for i in range(0, size):
        for j in range(i, size):
            if(maxProfit<highvalue_list[j]-lowvalue_list[i]):       # low_value 기준으로 profit 최대 지점 체크
                maxProfit=highvalue_list[j]-lowvalue_list[i]
                buy_date=date_list[i]
                sell_date=date_list[j]


    getResult.append(maxProfit)
    getResult.append(buy_date)
    getResult.append(sell_date)

    return getResult

###############################################################
# 당일날 BestValue-Lowvalue (TEMP Algorithm)

def dayBestOne():
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

    return queryset

###############################################################

def index(request):
    # 템플릿을 가져오는 코드
    template=loader.get_template('main/index.html')

    queryset=US_Stock.objects.values(
        'symbol', 'date', 'highvalue', 'lowvalue'
    ).order_by(
        'symbol', 'date'
    )

    
    symbol_result=[]        # symbol 저장 list
    maxProfit_result=[]     # maxProfit 저장 list
    buyDate_result=[]       # maxProfit을 낼 수 있는 buy date 저장 list
    sellDate_result=[]        # maxProfit을 낼 수 있는 sell date 저장 list

    compareStr="start"      # 비교 temp Str (symbol 구분 용도)

                                        # symbol 별로 date, highvalue, lowvalue 저장 변수
    date_list=[]
    highvalue_list=[]
    lowvalue_list=[]

    for i in queryset:
        presentSymbol=i['symbol']
        datevalue=to_integer(i['date'])
        presentHighValue=round(i['highvalue'], 2)
        presentLowValue=round(i['lowvalue'], 2)

        if(presentSymbol!=compareStr):                                              # 0~n-1 개의 symbol에 대해서 getProfit 체크
            symbol_result.append(presentSymbol)
            if(compareStr=="start"):
                compareStr=presentSymbol
            else:
                output=getMaxProfit(date_list, highvalue_list, lowvalue_list)
                maxProfit_result.append(round(output[0],2))
                buyDate_result.append(output[1])
                sellDate_result.append(output[2])
                date_list.clear()
                highvalue_list.clear()
                lowvalue_list.clear()
                compareStr=presentSymbol

        
        date_list.append(datevalue)
        highvalue_list.append(presentHighValue)
        lowvalue_list.append(presentLowValue)

    output=getMaxProfit(date_list, highvalue_list, lowvalue_list)       # 마지막 symbol에 대해서 get Profit 체크
    maxProfit_result.append(output[0])
    buyDate_result.append(output[1])
    sellDate_result.append(output[2])


    # template 으로 보내기 위한 데이터 재가공

    stockList=[]
    size=len(symbol_result)
    for i in range(0, size):
        stock_info={}
        stock_info['symbol']=symbol_result[i]
        stock_info['max_profit']=maxProfit_result[i]
        stock_info['buy_date']=buyDate_result[i]
        stock_info['sell_date']=sellDate_result[i]
        stockList.append(stock_info)
        #print(stock_info)

    context={
        'stocks' : stockList,
    }

    # 템플릿과 함께 가공한 템플릿 객체 넘기기
    return HttpResponse(template.render(context, request))

