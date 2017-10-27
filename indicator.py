import pymysql
from getandformat import *

def EMA(day,data):
	data = list(data)
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
	macd = []
	ema12 = EMA(day=12,data=data)
	ema26 = EMA(day=26,data=data)
	x = 0
	while x < len(ema26):           
		tmp = ema12[x+14] - ema26[x]
		# print ema12[x+14], ema26[x]
		# break
		macd.append(tmp)
		x = x +1
	macd = flaot2deciamal(macd)
	return macd

def RSI(day,data):
	data = list(data)
	GL=[]
	for x in range(1,len(data)):
		tmp = data[x]-data[x-1]
		GL.append(tmp)
	GL = flaot2deciamal(GL)
	G = 0.0
	L = 0.0
	AG = []
	AL = []
	for x in range(0,day-1):
		if GL[x] > 0.0:
			G = G + GL[x]
		else:
			L = L + GL[x]
	L = L*(-1)
	AG.append(G/day)
	AL.append(L/day)
	RS = AG[0]/AL[0]
	RSI = [0.0]
	RSI[0] = 100-(100/(1+RS))
	i = 1
	G = 0.0
	L = 0.0
	for x in range(day,len(data)):
		GL = data[x]-data[x-1]
		if GL < 0:
			L = GL*(-1)
			G = 0.0
		else:
			G = GL
			L = 0.0
		AG.append(((AG[i-1]*13)+G)/day)
		AL.append(((AL[i-1]*13)+L)/day)
		RS = AG[i]/AL[i]
		tmp = 100-(100/(1+RS))
		RSI.append(tmp)
		i+=1
	RSI = flaot2deciamal(RSI)
	return RSI
		

# data = getData("AAV") 
# data = getLast(data)
# data = [1559.35,1560.98,1566.92,1577.65,1576.68,1578.70,1586.79,1598.13,1591.65,1568.25,1543.67,1529.52,1478.97,1523.95,1544.03,1560.87,1544.57,1561.06]
# print(RSI(day=14,data = data))
# print(MACD(data = data))