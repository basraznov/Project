import indicator as indi
import format as gf
import buyorsell as bs
import sys

def diminput(Symblo):
    stock = gf.getData(Symblo)
    if len(stock) < 60:
        return None,None
    Last = gf.getLast(stock)
    Chper = gf.getChPer(stock)
    Vol = gf.getVol(stock)
    MACD = indi.MACD(Last)
    RSI = indi.RSI(data=Last,day=14)
    AvgVol = indi.AVGN(data=Vol,day=10)
    EMA5 = indi.EMA(data=Last,day=5)
    Date = gf.getDate(Symblo)
    answer = []
    Last = list(filter(lambda a: a != None, Last))
    for x in range(0,len(Last)):
        if x+1 == len(Last):
            answer.append("wwww")
            break
        rL = bs.findRange(Last[x+1],1)
        if Last[x] > rL[1]:
            answer.append("Sell")
        elif Last[x] < rL[0]:
            answer.append("Buy ")
        else:
            answer.append("Hold")
    answer.append(None)
    Elogic = [None]
    for x in range(0,len(Last)-1):
        buy = bs.buy(pLast=Last[x],nLast=Last[x+1],macd=MACD[x],avgVol=AvgVol[x],vol=Vol[x],nrsi=RSI[x+1],prsi=RSI[x])
        sell = bs.sell(pLast=Last[x],nLast=Last[x+1],avgVol=AvgVol[x],vol=Vol[x],ema=EMA5[x],pmacd=MACD[x],nmacd=MACD[x+1],nrsi=RSI[x+1],prsi=RSI[x])
        if buy == None or sell == None:
            Elogic.append(None)
        elif buy == False and sell == False:
            Elogic.append("Hold")
        elif buy == True and sell == False:
            Elogic.append("Buy ")
        elif buy == False and sell == True:
            Elogic.append("Sell")
        elif buy == True and sell == True:
            Elogic.append("Hold")
        else:
            Elogic.append("Error")
    dim = []
    temp = []
    k = 0
    for x in range(0,len(Last)):
        if(Last[x] == None):
            Last[x] = 0
        else:
            Last[x] = Last[x]
    Last = gf.flaot2deciamal(Last)

    for x in range(0,len(RSI)):
        if(RSI[x] == None):
            RSI[x] = 0
        RSI[x] = RSI[x]
    RSI = gf.flaot2deciamal(RSI)

    for x in range(0,len(Last)):
        if(RSI[x] == None or AvgVol[x] == None or MACD[x] == None or Elogic[x] == None):
            l=+1
            continue
        temp.append(Date[x])
        temp.append(Last[x])
        # temp.append(RSI[x])
        # temp.append(AvgVol[x])
        # temp.append(MACD[x])
        temp.append(Elogic[x])
        dim.append(temp)
        # print(temp)
        temp = []
        
    for x in range(0,len(answer)-len(dim)):
        answer.pop(0)
    answer.pop()
    return dim,answer


def connector(data1,data2):
    for x in range(0,len(data2)):
        data1.append(data2[x])
    return data1

def tranfromAnswer(answer):
    tmp = []
    for x in range(0,len(answer)):
        if answer[x] == -1:
            tmp.append([1,0,0])
        if answer[x] == 0:
            tmp.append([0,1,0])
        if answer[x] == 1:
            tmp.append([0,0,1])
    return tmp


def predic(Symblo):
    symbol = gf.allSymbol()
    th = symbol.index(Symblo)
    # print(th)
    # start = th
    data,answer = diminput(symbol[th])
    # labels = tranfromAnswer(answer)
    # SRAnswer = answer
    return data
    # stop = th
    # for x in range(start+1,stop):
    #     sys.stdout.write("Download progress: %.2f%%   \r" % (100*(x-start)/(stop-start)) )
    #     sys.stdout.flush()
    #     try:
    #         dataT,answerT = diminput(symbol[x])
    #         if dataT == None or answerT == None:
    #             continue
    #         labelsT =  tranfromAnswer(answerT)
    #         data = connector(data,dataT)
    #         labels = connector(labels,labelsT)
    #         SRAnswer = connector(SRAnswer,answerT)
    #     except Exception as e:
    #         print("Error in "+str(x)+" symbol is "+symbol[x])
    #         traceback.print_exc()
    #         exit()
    # print() 


k = predic("PTT")
for x in range(len(k)):
    print(k[x])




