# 주식 한 주를 사서 이득을 취할 수 있는 값 계산 사이트

<br>

## 참여자 및 참여 기간

- 최승진
- 2020.09.18~2020.09.20

<br>

## 토이 프로젝트 설명

- 특정 기간 동안 주식의 정보를 수집하여, 가장 큰 이득을 취할 수 있는 날을 출력하는 웹 사이트


<br>

## 파일 설명

- DB 수집 모듈을 별도로 구성 (inputData.py)
- US Stock symbol data (NASDAO.txt) (참고 : http://eoddata.com/stocklist/NYSE/A.htm)
- 패키지 version (version.txt)
- 웹 사이트 DB 연결 등 설정 (webservice > webservice.settings.py)
- DB TABLE에 매핑되는 ORM Object (webservice > webservice > main > models.py)
- ORM Object의 데이터를 가져와서 가공 및 알고리즘 구현 (webservice > webservice > main > views.py)
- 웹 사이트 HTML (webservice > webservice > main > templates > main > index.html)
- DB Table cap (db_table_cap.PNG)
- 웹 페이지의 메인 페이지 (result_cap.PNG)
- US Stock table의 일부 데이터 (us_stock.csv)

<br>

## 핵심 알고리즘 설명 (Get Biggest Profit)

- 단순 비교
- 데이터들이 Date를 오름차순으로 정렬되었다고 가정을 하고, 앞에서부터 low value를 기준으로 모든 high value list들의 값을 비교
- 시간복잡도 : O(N^2)

```python

low_value=[]
high_value=[]
maxProfit=0
for i in low_value:
  for j in (i, len(high_value)):
     maxProfit=max(maxProfit, high_value[j]-low_value[i])

```

- O(N^2)으로 전체 탐색을 해야할 것이라고 생각한 이유는 한 가지입니다. 슬라이딩 윈도우를 사용하여 연속적인 Value에 대해서 비교를 하거나 Priority_queue를 사용하여 결과값을 도출할 경우 예외가 발생할 것이라고 생각했기 때문입니다. 실제로 hight value가 가장 큰 값에 해당하는 date가 low value가 가장 적은 값에 해당하는 data보다 먼저 일어난 testcase가 있을 경우 low value에 대해서 기억을 하지 못하기 때문에 예외가 발생할 것이라고 판단하였습니다.

<br>
<br>


## 또 다른 알고리즘 (시간복잡도 : O(N))

- 위의 알고리즘의 경우 사는 날의 기준으로 주식을 한 주를 사서 최대 이익을 낼 수 있는 파는 날을 찾는 과정이라면, 반대로 파는 날을 기준으로 보면 어떨까라는 생각에 생각한 알고리즘

```python

def max_profit(prices):
  n=len(prices)
  max_profit=0
  min_prices=prices[0]
  
  for i in range(1,n):
    profit=pries[i]-min_prices
    if(profit>max_profit):
      max_profit=profit
    if(pries[i]<min_price):
      min_prices=prices[i]
    
   return max_profit
   
```

<br>
<br>

## 추가사항

- 그래프 : TABLE에 있는 모든 Symbol들에 대해서 하루에 사고 팔고의 max_profit, min_profit 을 그래프로 시각화한 것

<br>
<br>


## 제한사항

- 오래 걸리는 DB INSERT
  > AWS RDS를 Server DB구축으로 인하여 DB INSERT가 오래걸리는 문제 발생 + 네트워크 문제
  > 추가적인 문제 파악 중
  
- 수많은 데이터에 대해서 처리를 하면서 발생하는 시간복잡도로 인하여 느린 웹 페이지 로딩 속도
  > Symbol 개수 1820개, DATA 개수 25만개
  
  > Get Biggest Profit 시간복잡도 O(N^2)
  
  > 여기에서 N : 126, 180일동안 Stock 개수 : 126
  
  > 시간복잡도 = 126*126*1820 = 28,894,32 = 약 3천만
  
  > 추가적으로 효율적인 알고리즘에 대해 고민 중
  
  
      > 2번째로 생각한 알고리즘으로 시간복잡도 126*1820 = 100만
   

