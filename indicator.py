import MySQLdb


def flaot2deciamal(data):
	data = [ '%.3f' % elem for elem in data ]
	data = [float(i) for i in data]
	return data

def getLast(data):
	newdata=[]
	for x in range(0,len(data)):
		newdata.append(data[x][5])
	return newdata


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
		sma = sma + data[day-x]	
	sma = sma/day
	ema = []
	ema.append(sma)
	i = 1
	k = day + i
	while k < len(data):
		k = day+i 
		tmp = ema[i-1]+(2.0/(day+1))*(data[k-1]-ema[i-1])
		ema.append(tmp)
		i = i+1
	ema = flaot2deciamal(ema)
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
	macd = flaot2deciamal(macd)
	return macd

def RSI(day,data):
	GL=[0.0]
	print data[0][5],
	for x in range(1,len(data)):
		print data[x][5],
		tmp = data[x][5]-data[x-1][5]
		GL.append(tmp)
	GL = flaot2deciamal(GL)
	AG = 0.0
	AL = 0.0
	for x in range(0,day):
		if GL[x] > 0.0:
			AG = AG + GL[x]
		else:
			AL = AL + GL[x]
	AG = AG/day
	AL = AL/day
	RS = AG/AL
	print AG,AL,RS
	RSI = [0.0]
	RSI[0] = 100-(100/(1+RS))
	print RSI[0]



data = getData("AAV")
#print getLast(data)
print EMA(5,[11,12,13,14,15,16,17])
# RSI(day=14,data = data)