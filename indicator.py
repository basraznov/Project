import MySQLdb



def getData(Symbol):
	db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
	sql = "SELECT * FROM `trade` WHERE Symbol = %s"
	data=[Symbol]
	cursor = db.cursor()
	cursor.execute(sql,data)
	results = cursor.fetchall()
	return results

def EMA(day,data):
	sma = 0.0
	for x in range(1,day+1):
		sma = sma + data[day-x][5]	
	sma = sma/day
	ema = []
	ema.append(sma)
	#for i in range(1,len(data)):
	i = 1
	k = day + i
	while k < len(data):
		k = day+i 
		tmp = ema[i-1]+(2.0/(day+1))*(data[k-1][5]-ema[i-1])
		ema.append(tmp)
		i = i+1
	print ema 
			

data = getData("AAV")
EMA(day=5,data=data)