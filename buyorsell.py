
# ราคาปิดของวันนี้ >= ราคาปิดของเมื่อวาน (ซื้อหรือถือ)
#     vol สูงเกินค่าเฉลี่ย
#         MACD +
#             RSI > 30 and RSI < 70
#             ซื้อ
#     ถือ

# ราคาปิดของวันนี้ < ราคาปิดของเมื่อวาน (ถือหรือขาย)
#     vol สูงเกินค่าเฉลี่ย
#         ขาย
#     ราคาปิด < EMA
#         ขาย
#     ถือ

import pymysql
from format import *

def findRange(num,per):
	return [num-(num*per/100),num+(num*per/100)]

def between(short,long,number):
	if(number >= short and number <= long):
		return True
	else:
		return False

def buy(pLast,nLast,macd,rsi,avgVol,vol):
	if(pLast == None or nLast == None or macd == None or rsi == None or avgVol == None or vol == None):
		return None
	rL = findRange(pLast,10)
	rV = findRange(avgVol,15)
	if(nLast >= rL[0]):
		if(vol > rV[1]):
			if(rsi <= 65):
				return	True
	return False

def sell(pLast,nLast,avgVol,vol,ema):
	if(pLast == None or nLast == None or avgVol == None or vol == None or ema == None):
		return None
	rL = findRange(pLast,10)
	rV = findRange(avgVol,15)
	rE = findRange(ema,10)
	if(nLast < rL[1]):
		if(vol > rV[1]):
			return True
		if(nLast < rE[1]):
			return True
	return False

# macd = 0.007
# rsi = 45.791
# pLast = 6.4
# nLast = 6.4
# vol = 12335927
# avgVol = 40013446.6834
# ema5 = 6.42

# if buy(pLast=pLast,nLast=nLast,macd=macd,rsi=rsi,avgVol=avgVol,vol=vol):
# 	print("Buy")
# elif sell(pLast=pLast,nLast=nLast,avgVol=avgVol,vol=vol,ema=ema5):
# 	print("Sell")
# else:
# 	print("Nothing")
