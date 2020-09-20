import pandas_datareader as pdr
from datetime import datetime
from datetime import timedelta
import pymysql
import time

def getSymbolName():
    # readline all
    # parsing name

    f=open("NASDAQ.txt", "r")

    list = []
    while True:
        line=f.readline()
        if not line:
            break
        
        word=line.split('\t')
        name=word[0]
        list.append(name)
    f.close()
    return list

    # first element value is not name -> (1, length)
    # list : name List ex) GOOG, GOOGL

def insertData(list, conn):
    startTime=time.time()
    length=len(list)
    for i in range(1, length):
        curs=conn.cursor()
        # presentTime
        presentTime=datetime.today()
        #print(presentTime)

        # presentTime data parsing (year, month, day)
        # yesterday + 179 = 180
        # today=yesterday
        today=datetime(presentTime.year, presentTime.month, presentTime.day)
        today=today-timedelta(days=1)
        #print(today)

        # before_180 = today - days 180
        before_180=today-timedelta(days=180)
        #print(before_180)

        # try if there is no error with date 
        try:
            df = pdr.get_data_yahoo(list[i], before_180, today)
        except: # if there is no data in (before_180~today) skip
            continue
        
        #print(df)

        df_index=df.index

        df_length=len(df)
        symbol=list[i]
        #print(symbol+"\t"+str(df_length))
        #print(df.loc[dates[0]])
        print(symbol)
        
        for j in range(0, df_length):
            dateValue=df_index[j]
            loc=df.iloc[j]
            loc_length=len(loc)
            dateValue=dateValue.to_pydatetime()
            #print(type(dateValue))
            highValue=loc[0]
            lowValue=loc[1]
            openValue=loc[2]
            closeValue=loc[3]
            volumeValue=loc[4]
            adjcloseValue=loc[5]

            
            sql='''INSERT INTO US_Stock(symbol, date, highvalue, lowvalue, openvalue, closevalue, volumevalue, adjclosevalue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            #test data
            #curs.execute(sql, ("AACC", "2019-01-03", 1.1, 1.1, 1.1, 1.1, 1.1, 1.1))
            curs.execute(sql,  (symbol, dateValue, float(highValue), float(lowValue), float(openValue), float(closeValue), float(volumeValue), float(adjcloseValue)))

            # symbol, dateValue, highValue, lowValue, openValue, closeValue, volumeValue, adjcloseValue
            #'''INSERT INTO US_Stock(symbol, date, highvalue, lowvalue, openvalue, closevalue, volumevalue, adjclosevalue) VALUES (symbol, dateValue, highValue, lowValue, openValue, closeValue, volumeValue, adjcloseValue)'''
        conn.commit()

    endTime=time.time()
    costTime=endTime-startTime
    print(costTime)
    conn.close()

def dbConnection():
    conn = pymysql.connect(host='**************', user='**************', password='**************', db='**************')
    return conn;

def testTime():
    startTime=time.time()
    a=0
    for i in range(0, 100000):
        a=a+1
    endTime=time.time()

    print(startTime)
    print(endTime)
    costTime=endTime-startTime
    print(costTime)
    #costTime=endTime.timedelta()

def main():
    list=getSymbolName()
    conn=dbConnection()
    #testTime()
    #print(conn)
    insertData(list, conn)

if __name__=="__main__":
    main()
