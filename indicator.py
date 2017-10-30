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
	G = []
	L = []
	for x in GL:
		if x >= 0:
			G.append(x)
			L.append(0)
		else:
			G.append(0)
			L.append(x*(-1))
	AG = []
	AL = []
	RS = []
	RSI = []
	SG = 0.0
	SL = 0.0
	for x in range(0,day):
		SG += G[x]
		SL += L[x]
	AG.append(SG/day)
	AG = flaot2deciamal(AG)
	AL.append(SL/day)
	AL = flaot2deciamal(AL)
	RS.append(AG[0]/AL[0])
	RS = flaot2deciamal(RS)
	RSI.append(100-(100/(1+RS[0])))
	RSI = flaot2deciamal(RSI)
	#print(x,data[x],G[x-1],L[x-1],AG[x-day],AL[x-day],RS[-1],RSI[-1])
	x = day+1
	while(x < len(data)):
		AG.append((AG[x-day-1]*13+G[x-1])/14)
		AG = flaot2deciamal(AG)
		AL.append((AL[x-day-1]*13+L[x-1])/14)
		AL = flaot2deciamal(AL)
		RS.append(AG[-1]/AL[-1])
		RS = flaot2deciamal(RS)
		RSI.append(100-(100/(1+RS[-1])))
		RSI = flaot2deciamal(RSI)
		x += 1
	return RSI
		

		
def AVG(data):
	data = list(data)
	sum = 0.0
	for x in data:
		sum += x
	avg = sum/len(data)
	return avg



AAV = getData("AAV")
# data = getVol(data)
# avgVol = AVG(data)
AAV = getLast(AAV)
# data = [1559.35,1560.98,1566.92,1577.65,1576.68,1578.70,1586.79,1598.13,1591.65,1568.25,1543.67,1529.52,1478.97,1523.95,1544.03,1560.87,1544.57,1561.06]
# print(EMA(day=5,data=data))
#print(data)
data = [46.1250,47.1250,46.4375,46.9375,44.9375,44.2500,44.6250,45.7500,47.8125,47.5625,47.0000,44.5625,46.3125,47.6875,46.6875,45.6875,43.0625,43.5625,44.8750,43.6875]
print(RSI(day=10,data = AAV))
#print(MACD(data = AAV))	