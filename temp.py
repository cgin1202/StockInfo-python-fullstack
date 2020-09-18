import pandas_datareader as pdr
from datetime import datetime
from datetime import timedelta

# presentTime
presentTime=datetime.today()
#print(presentTime)

# presentTime data parsing (year, month, day)
# yesterday + 179 = 180
# today=yesterday
today=datetime(presentTime.year, presentTime.month, presentTime.day)
today=today-timedelta(days=1)
print(today)

# before_180 = today - days 180
before_180=today-timedelta(days=180)
print(before_180)


df = pdr.get_data_yahoo('AACQ', before_180, today)
print(df)