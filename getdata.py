import requests
from lxml import html
import re
import MySQLdb
from datetime import datetime
import sys

SETCSurl = 'https://marketdata.set.or.th/mkt/commonstocklistresult.do?market=SET&type=S'#SET Common Stocks
SETWurl = 'https://marketdata.set.or.th/mkt/stocklistbytype.do?market=SET&language=en&country=US&type=W' #SET Warrants
MAICSurl = 'https://marketdata.set.or.th/mkt/commonstocklistresult.do?market=mai&type=S'#MAI Common Stocks
MAIWurl = 'https://marketdata.set.or.th/mkt/stocklistbytype.do?market=mai&language=en&country=US&type=W' #MAI Warrants

url = [SETCSurl,SETWurl,MAICSurl,MAIWurl]
def ShowData(data):
    for x in range(len(data)):
        print data[x]

def FormatData(list):
    w=11
    h=1
    data = [['' for x in range(w)] for y in range(h)]
    i = 0
    Symbol = 0
    x = 0
    count = 0
    while x < len(list):
        if list[x] == 'SET' or list[x] == 'SET50' or list[x] == 'SET100' or list[x] == 'sSET' or list[x] == 'SETHD' or list[x] == 'mai':
            x = x + 8
            continue
        else:
            if (list[x].find(' ') != -1 or list[x] == 'SP' or list[x] == 'NP' or list[x] == 'XR' or list[x] == 'XD' or list[x] == 'XA' or list[x] == 'XW') and list[x] != 'S & J':
                x = x + 1
                continue

            data[Symbol][i] = list[x]
            i=i+1
            if i%w == 0:
                if data[Symbol][i-1] != '-':
                    data[Symbol][i-1] = int(float(data[Symbol][i-1])*1000)
                blank = ['']*w
                data.append(blank)
                Symbol = Symbol+1
                i = 0
                count = count +1 
            x = x + 1
    return data

def Getdate(url):
    r = requests.get(url)
    tree = html.fromstring(r.content)
    element = tree.xpath('//div[@class="table-responsive"]/table/tbody/tr/td//text()')
    stocks = [re.sub("\n\r|\n|\r", '', x) for x in element]
    stocks = [x.replace(",","") for x in stocks]
    stocks = [x.strip(' ') for x in stocks]
    stocks = filter(None,stocks)
    return stocks

def tosql(list):
    mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
    date = str(datetime.now()).split(" ")[0]
    for x in range(len(list)-1):
        data = [date,list[x][0],list[x][1],list[x][2],list[x][3],list[x][4],list[x][6],list[x][9],list[x][10]]
        for y in range(len(data)):
            if data[y] == '-' or data[y] == 'N/A':
                data[y] = None
        cursor = mydb.cursor()
        sql = 'INSERT INTO trade(`Date`,`Symbol`,`Open`,`High`,`Low`,`Last`,`ChPer`,`Volumn`,`Money`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,data)
        mydb.commit()
    cursor.close()



stocks = Getdate(url[int(sys.argv[1])-1])
data = FormatData(stocks)
ShowData(data)
raw_input("Press Enter to continue...")
tosql(data)
print "############################# Done ##############################"
