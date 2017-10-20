import requests
from lxml import html
import re
import MySQLdb
from datetime import datetime
import sys

SETCSurl = 'https://marketdata.set.or.th/mkt/commonstocklistresult.do?market=SET&type=S'#SET Common Stocks 1
SETWurl = 'https://marketdata.set.or.th/mkt/stocklistbytype.do?market=SET&language=en&country=US&type=W' #SET Warrants 2
MAICSurl = 'https://marketdata.set.or.th/mkt/commonstocklistresult.do?market=mai&type=S'#MAI Common Stocks 3
MAIWurl = 'https://marketdata.set.or.th/mkt/stocklistbytype.do?market=mai&language=en&country=US&type=W' #MAI Warrants 4

url = [SETCSurl,SETWurl,MAICSurl,MAIWurl]
def ShowData(data):
    for x in range(len(data)):
        print (data[x])

def FormatData(input):
    w=11
    h=1
    data = [['' for x in range(w)] for y in range(h)]
    i = 0
    Symbol = 0
    x = 0
    count = 0
    input = list(input)
    while x < len(input):
        if input[x] == 'SET' or input[x] == 'SET50' or input[x] == 'SET100' or input[x] == 'sSET' or input[x] == 'SETHD' or input[x] == 'mai':
            x = x + 8
            continue
        else:
            if (input[x].find(' ') != -1 or input[x] == 'SP' or input[x] == 'NP' or input[x] == 'XR' or input[x] == 'XD' or input[x] == 'XA' or input[x] == 'XW') and input[x] != 'S & J':
                x = x + 1
                continue

            data[Symbol][i] = input[x]
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

def GetdateFromWeb(url):
    r = requests.get(url)
    tree = html.fromstring(r.content)
    element = tree.xpath('//div[@class="table-responsive"]/table/tbody/tr/td//text()')
    stocks = [re.sub("\n\r|\n|\r", '', x) for x in element]
    stocks = [x.replace(",","") for x in stocks]
    stocks = [x.strip(' ') for x in stocks]
    stocks = filter(None,stocks)
    return stocks

def addNewCompany(symbol):
    mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
    sql = "SELECT * from `company` where Symbol = %s"
    data = [symbol]
    cursor = mydb.cursor()
    cursor.execute(sql,data)
    results = cursor.fetchall()
    row = cursor.rowcount
    if row == 0:
        url = 'https://www.set.or.th/set/companyprofile.do?symbol='+symbol+'&ssoPageId=4&language=en&country=US'
        r = requests.get(url)
        if 'color:red' in r.content:
            print ("Error can't find Symbol [",symbol,"]")
            return False
        tree = html.fromstring(r.content)
        element = tree.xpath('//table[@class="table"]/tr/td/div/div//text()')
        element = [re.sub("\n\r|\n|\r", '', x) for x in element]
        element = [x.strip(' ') for x in element]
        element = filter(None,element)
        companyName = None
        market = None
        industry = None
        sector = None
        for x in range(0,len(element)):
            if element[x] == 'Company Name' and element[x+1] != '-':
                companyName =  element[x+1]
            if element[x] == 'Market' and element[x+1] != '-':
                market = element[x+1]
            if element[x] == 'Industry' and element[x+1] != '-':
                industry = element[x+1]
            if element[x] == 'Sector' and element[x+1] != '-':
                sector = element[x+1]
        
        sql = 'INSERT INTO `company`(`Symbol`, `Company`, `Market`, `Industry`, `Sector`, `MySector`, `ESector`, `SET50`, `SET100`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        data = [symbol,companyName,market,industry,sector,None,None,None,None]
        cursor = mydb.cursor()
        cursor.execute(sql,data)
        mydb.commit()
        cursor.close()
        return True
    else:
        print ("Error Check your database symbol = ",symbol," is appear on database")
        print (results)
        return False

def tosql(input):
    input = list(input)
    name = []
    mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
    date = str(datetime.now()).split(" ")[0]
    for x in range(len(input)-1):
        data = [date,input[x][0],input[x][1],input[x][2],input[x][3],input[x][4],input[x][6],input[x][9],input[x][10]]
        for y in range(len(data)):
            if data[y] == '-' or data[y] == 'N/A':
                if data[y] == 'N/A':
                    name.append(data[y-5])
                data[y] = None
        cursor = mydb.cursor()
        sql = 'INSERT INTO trade(`Date`,`Symbol`,`Open`,`High`,`Low`,`Last`,`ChPer`,`Volumn`,`Money`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,data)
        mydb.commit()
    cursor.close()
    print ("############################# Done ##############################")
    if name:
        input("Press Enter to auto add company or ctrl+c to exit")
        for x in name:
            print ("Adding new Symbol [",x,"]")
            if addNewCompany(x):
                print ("Adding Symbol [",x,"] success")
            else:
                print ("Addin Symbol [",x,"] Fail")



       

stocks = GetdateFromWeb(url[int(sys.argv[1])-1])
data = FormatData(stocks)
ShowData(data)
input("Press Enter for add data into database or ctrl+c to exit")
tosql(data)

