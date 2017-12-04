import pymysql

def flaot2deciamal(data):
	data = [ '%.3f' % elem for elem in data ]
	data = [float(i) for i in data]
	return data

def getLast(data):
	data = list(data)
	newdata=[]
	for x in range(0,len(data)):
		newdata.append(data[x][5])
	return newdata


def getData(Symbol):
	db = pymysql.connect(host='127.0.0.1',user='root',passwd='',db='Project')
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
		newdata.append(data[x][7])
	return newdata

def getChPer(data):
	data = list(data)
	newdata=[]
	for x in range(0,len(data)):
		newdata.append(data[x][6])
	return newdata


data = getData("AAV")
data = getVol(data)

