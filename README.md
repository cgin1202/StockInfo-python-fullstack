# Get Max profit over the last 180 days

<br>
## 요구조건

- data : US Stock Symbol
- only one single buy and sell
- API, Business and data layer 분리
- 재사용 가능한 Module
- DB 수집 API 변경이 쉬운 Module로 구성


<br>
## 실행 방법

- version.txt에 있는데 패키지 설치
- Anaconda prompt를 실행하고 > webservice 폴더 안으로 이동
- 'python manage.py runserver' 명령어 입력
- 브라우저 > 'http://127.0.0.1:8000/main ' url 입력


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
  
  
   

