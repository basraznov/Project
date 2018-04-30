import pymysql
import re
import init as it


def flaot2deciamal(data):
	data = [ '%.3f' % elem for elem in data ]
	data = [float(i) for i in data]
	return data

def getLast(data):
	data = list(data)
	newdata=[]
	for x in range(0,len(data)):
		if data[x][5] == None:
			continue
		newdata.append(data[x][5])
	return newdata


def getData(Symbol):
	db = pymysql.connect(host=it.hostip,user=it.userdatebase,passwd=it.passdatabase,db=it.datebasename)
	# sql = "SELECT * FROM `trade` WHERE Symbol = %s and date <= '2017-01-01'"
	sql = "SELECT * FROM `trade` WHERE Symbol = %s"
	data=[Symbol]
	cursor = db.cursor()
	cursor.execute(sql,data)
	results = cursor.fetchall()
	return results

def getVol(data):
	data = list(data)
	newdata=[]
	for x in range(0,len(data)):
		if data[x][5] == None:
			continue
		newdata.append(data[x][7])
	return newdata

def getChPer(data):
	data = list(data)
	newdata=[]
	for x in range(0,len(data)):
		if data[x][5] == None:
			continue
		newdata.append(data[x][6])
	return newdata

def Normaliz(data,avg):
	data = list(data)
	newdata = []
	for x in range(0,len(data)):
		newdata.append(data[x]/(avg+data[x]))
	newdata = flaot2deciamal(newdata)
	return newdata

def AVG(data):
	data = list(data)
	sum = 0.0
	for x in data:
		sum += x
	avg = sum/len(data)
	return avg

def allSymbol():
	db = pymysql.connect(host=it.hostip,user=it.userdatebase,passwd=it.passdatabase,db=it.datebasename)
	sql = "SELECT DISTINCT Symbol from trade"
	cursor = db.cursor()
	cursor.execute(sql)
	results = cursor.fetchall()
	results = [str(i) for i in results]
	results = [re.sub(",|\'|\(|\)", '', x) for x in results]
	return results

def getDate(Symbol):
	db = pymysql.connect(host=it.hostip,user=it.userdatebase,passwd=it.passdatabase,db=it.datebasename)
	# sql = "SELECT date,last FROM `trade` WHERE Symbol = %s and date <= '2018-01-01'"
	sql = "SELECT * FROM `trade` WHERE Symbol = %s"
	data=[Symbol]
	cursor = db.cursor()
	cursor.execute(sql,data)
	results = cursor.fetchall()
	results = list(results)
	k = results
	x = 0
	while True:
		if x == len(results):
			break
		if results[x][1] == None:
			results.pop(x)
			continue
		results[x] = list(results[x])
		x += 1
	results = list(results)
	results = [results.pop(0) for results in results]
	return results
