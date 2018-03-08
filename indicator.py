import pymysql
from format import *

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
	for x in range(0,day-1):
		ema.insert(0, None)
	return ema

def MACD(data):
	macd = []
	ema12 = EMA(day=12,data=data)
	ema12 = list(filter(lambda a: a != None, ema12))
	ema26 = EMA(day=26,data=data)
	ema26 = list(filter(lambda a: a != None, ema26))
	x = 0
	while x < len(ema26):
		tmp = ema12[x+14] - ema26[x]
		macd.append(tmp)
		x = x +1
	macd = flaot2deciamal(macd)
	for x in range(0,25):
		macd.insert(0,None)
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
	# return None
	AG.append(SG/day)
	AG = flaot2deciamal(AG)
	AL.append(SL/day)
	AL = flaot2deciamal(AL)
	if AL[0] == 0:
		AL[0] = 0.000000001
	RS.append(AG[0]/AL[0])
	RS = flaot2deciamal(RS)
	RSI.append(100-(100/(1+RS[0])))
	RSI = flaot2deciamal(RSI)
	x = day+1
	while(x < len(data)):
		AG.append((AG[x-day-1]*13+G[x-1])/14)
		AG = flaot2deciamal(AG)
		AL.append((AL[x-day-1]*13+L[x-1])/14)
		AL = flaot2deciamal(AL)
		if AL[-1] == 0:
			AL[-1] = 0.000000001
		RS.append(AG[-1]/AL[-1])
		RS = flaot2deciamal(RS)
		RSI.append(100-(100/(1+RS[-1])))
		RSI = flaot2deciamal(RSI)
		x += 1
	for x in range(0,day):
		RSI.insert(0,None)
	return RSI
		

		
def AVG(data):
	data = list(data)
	sum = 0.0
	for x in data:
		sum += x
	avg = sum/len(data)
	return avg

def AVGN(day,data):
	data = list(data)
	temp = 0.0
	avgn=[]
	for x in range(0,day-1):
		avgn.append(None)
	for x in range(day,len(data)+1):
		for y in range(x-day,x):
			if(data[y] == None):
				avgn.append(None)
				continue
			temp += data[y]
		avgn.append(temp/day)
		temp = 0.0
	return avgn



# data = [10,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,10,10]
# print(len(data))
# print(AVGN(day = 10,data = data))
# print(len(AVGN(day = 10,data = data)))
# data = getData("CGS")
# data = getVol(data)
# avgVol = AVG(data)
# Last = getLast(data)
# print(Last)
# for x in data:
# 	print(x)
# print(data)
# data = [1559.35,1560.98,1566.92,1577.65,1576.68,1578.70,1586.79,1598.13,1591.65,1568.25,1543.67,1529.52,1478.97,1523.95,1544.03,1560.87,1544.57,1561.06]
# print(EMA(day=5,data=Last))
# data = [22.27,22.19,22.08,22.17,22.18,22.13,22.23,22.43,22.24,22.29,22.15,22.39,22.38,22.61,23.36,24.05]
# print(MACD(data = data))
# print(RSI(data=Last,day=14))
# print(MACD(data = data))	