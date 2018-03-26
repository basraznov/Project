import numpy as np
import indicator as indi
import format as gf
import buyorsell as bs
import sys
import traceback
import random
import datetime
import multiprocessing

AllFeature = 6


def collectFinal(Symbol):
    stock = gf.getData(Symbol)
    Date = gf.getDate(Symbol)
    if not Date:
        return None
    day = (datetime.datetime.now().date()-Date[-1]).days
    if len(stock) < 60 or day > 2:
        return None
    Last = gf.getLast(stock)
    AvgLast = indi.AVGN(data=Last,day=5)
    AvgLast10 = indi.AVGN(data=Last,day=10)
    Chper = gf.getChPer(stock)
    Vol = gf.getVol(stock)
    MACD = indi.MACD(Last)
    MACDAvg10 = indi.AVGN(data=MACD,day=10)
    RSI = indi.RSI(data=Last,day=14)
    AvgVol = indi.AVGN(data=Vol,day=5)
    AvgVol10 = indi.AVGN(data=Vol,day=10)
    EMA5 = indi.EMA(data=Last,day=5)
    

    Last = list(filter(lambda a: a != None, Last))
    Elogic = [None]
    for x in range(0,len(Last)-1):
        buy = bs.buy(pLast=Last[x],nLast=Last[x+1],macd=MACD[x],avgVol=AvgVol[x],vol=Vol[x],nrsi=RSI[x+1],prsi=RSI[x])
        sell = bs.sell(pLast=Last[x],nLast=Last[x+1],avgVol=AvgVol[x],vol=Vol[x],ema=EMA5[x],pmacd=MACD[x],nmacd=MACD[x+1],nrsi=RSI[x+1],prsi=RSI[x])
        if buy == None or sell == None:
            Elogic.append(None)
        elif buy == False and sell == False:
            Elogic.append(0)
        elif buy == True and sell == False:
            Elogic.append(1)
        elif buy == False and sell == True:
            Elogic.append(0)
        elif buy == True and sell == True:
            Elogic.append(0)
        else:
            Elogic.append(9)
    dim = []
    temp = []
    for x in range(0,len(Chper)):
        if(Chper[x] == None):
            Chper[x] = 0
        elif Chper[x] > 0:
            Chper[x] = 0
        else:
            Chper[x] = 1
    RSIM = []
    RSI70 = []
    RSI30 = []
    for x in range(0,len(RSI)):
        if(RSI[x] == None):
            RSI[x] = 0
        if RSI[x] > 30:
            RSI30.append(1)
            RSI70.append(0)
        elif RSI[x] < 70:
            RSI70.append(1)
            RSI30.append(0)
        if x != 0:
            if RSI[x] > RSI[x-1]:
                RSIM.append(1)
            else:
                RSIM.append(0)
        else:
            RSIM.append(0)

    for x in range(0,len(AvgLast10)):
        if(AvgLast10[x] == None):
            AvgLast10[x] = 0.00
    AvgLast10 = gf.flaot2deciamal(AvgLast10)

    for x in range(0,len(Elogic)):
        if(Elogic[x] == None):
            Elogic[x] = 0
    Elogic = gf.flaot2deciamal(Elogic)

    for x in range(0,len(AvgVol10)):
        if(AvgVol10[x] == None):
            AvgVol10[x] = 0
    AvgVol10 = gf.flaot2deciamal(AvgVol10)
    

    AvgVolM = []
    for x in range(0,len(AvgVol)):
        if(AvgVol[x] == None):
            AvgVol[x] = 0
        if x != 0:
            if AvgVol[x] > AvgVol10[x-1]:
                AvgVolM.append(1)
            else:
                AvgVolM.append(0)
        else:
            AvgVolM.append(0)

    Last10Avg = []
    for x in range(0,len(Last)):
        if(Last[x] == None):
            Last[x] = 0
        if x != 0:
            if AvgLast10[x-1] > Last[x]:
                Last10Avg.append(0)
            else:
                Last10Avg.append(1)
        else:
            Last10Avg.append(0)

    for x in range(0,len(Last)):
        temp.append(RSIM[x])
        temp.append(RSI70[x])
        temp.append(RSI30[x])
        temp.append(AvgVolM[x])
        temp.append(Last10Avg[x])
        temp.append(Elogic[x])
        dim.append(temp)
        temp = []

    return dim[len(dim)-1]


listSymbol = gf.allSymbol()
testset = []
# time = datetime.datetime.now()
for x in range(len(listSymbol)):
    k = collectFinal(listSymbol[x])
    if k == None:
        continue
    # print(k,listSymbol[x])
    testset.append(k)
print(testset)
donetime = datetime.datetime.now()
# print(donetime-time)
