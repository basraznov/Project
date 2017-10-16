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
	i = 1
	k = day + i
	while k < len(data):
		k = day+i 
		tmp = ema[i-1]+(2.0/(day+1))*(data[k-1][5]-ema[i-1])
		ema.append(tmp)
		i = i+1
	return ema

def MACD(data):
	macd = [0.0]
	ema12 = EMA(day=12,data=data)
	ema26 = EMA(day=26,data=data)
	macd[0] = float(ema12[0]-ema26[0])
	x = 1
	while x < len(ema26):
		tmp = ema12[x+14] - ema26[x]
		macd.append(tmp)
		x = x +1 
	return macd

def RSI(data):
	

data = getData("AAV")
MACD(data = data)