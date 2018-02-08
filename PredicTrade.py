import indicator as indi
import format as gf
import buyorsell as bs
import sys
import traceback

a = 0
b = 0
c = 0
d = 0
e = 0
f = 0

def diminput(Symblo):
    global a
    global b
    global c
    global d
    global e
    global f
    
    stock = gf.getData(Symblo)
    if len(stock) < 60:
        return None,None
    Last = gf.getLast(stock)
    Chper = gf.getChPer(stock)
    Vol = gf.getVol(stock)
    MACD = indi.MACD(Last)
    RSI = indi.RSI(data=Last,day=14)
    AvgVol = indi.AVG(Vol)
    NomalZ = gf.Normaliz(data=Vol,avg= AvgVol)
    EMA5 = indi.EMA(data=Last,day=5)
    Date = gf.getDate(Symblo)
    answer = []
    Last = list(filter(lambda a: a != None, Last))
    for x in range(0,len(Last)-1):
        rL = bs.findRange(Last[x+1],0.5)
        if Last[x] > rL[1]:
            answer.append("Sell")
        elif Last[x] < rL[0]:
            answer.append("Buy ")
        else:
            answer.append("Hold")
    answer.append(None)
    Elogic = [None]
    for x in range(0,len(Last)-1):
        buy = bs.buy(pLast=Last[x],nLast=Last[x+1],macd=MACD[x],rsi=RSI[x],avgVol=AvgVol,vol=Vol[x])
        sell = bs.sell(pLast=Last[x],nLast=Last[x+1],avgVol=AvgVol,vol=Vol[x],ema=EMA5[x],macd=MACD[x])
        if buy == None or sell == None:
            Elogic.append(None)
        elif buy == False and sell == False:
            a += 1
            Elogic.append("Hold")
        elif buy == True and sell == False:
            b += 1
            Elogic.append("Buy ")
        elif buy == False and sell == True:
            c += 1
            Elogic.append("Sell")
        elif buy == True and sell == True:
            d += 1
            Elogic.append("Hold")
        else:
            Elogic.append("Error")
        if buy == True:
            e += 1
        if sell == True:
            f += 1
    dim = []
    temp = []
    k = 0
    for x in range(0,len(Chper)):
        if(Chper[x] == None):
            Chper[x] = 0
        else:
            Chper[x] = Chper[x]
    Chper = gf.flaot2deciamal(Chper)

    for x in range(0,len(RSI)):
        if(RSI[x] == None):
            RSI[x] = 0
        RSI[x] = RSI[x]
    RSI = gf.flaot2deciamal(RSI)

    for x in range(0,len(Last)):
        if(RSI[x] == None or NomalZ[x] == None or MACD[x] == None or Elogic[x] == None):
            l=+1
            continue
        temp.append(Date[x])
        temp.append(Chper[x])
        temp.append(RSI[x])
        temp.append(NomalZ[x])
        temp.append(MACD[x])
        temp.append(Elogic[x])
        dim.append(temp)
        temp = []
    for x in range(0,len(answer)-len(dim)):
        answer.pop(0)
    answer.pop()
    dim.pop()
    for x in range(0,len(dim)):
        print(x,dim[x])
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


symbol = gf.allSymbol()
th = symbol.index("TOP")
print(th)
start = th
data,answer = diminput(symbol[start])
labels = tranfromAnswer(answer)
SRAnswer = answer
stop = th
for x in range(start+1,stop):
    sys.stdout.write("Download progress: %.2f%%   \r" % (100*(x-start)/(stop-start)) )
    sys.stdout.flush()
    try:
        dataT,answerT = diminput(symbol[x])
        if dataT == None or answerT == None:
            continue
        labelsT =  tranfromAnswer(answerT)
        data = connector(data,dataT)
        labels = connector(labels,labelsT)
        SRAnswer = connector(SRAnswer,answerT)
    except Exception as e:
        print("Error in "+str(x)+" symbol is "+symbol[x])
        traceback.print_exc()
        exit()
print()
k = 0
j = 0
l = 0
m = 0
p = 1
for x in range(0,len(data)-1):
    if (data[x][5]) == answer[x]:
        k+=1
    if answer[x] == "Buy ":
        l+=1
    if answer[x] == "Hold":
        j+=1
    if answer[x] == "Sell":
        m+=1
    p += 1
print(k,len(data),k/len(data))
print(l,j,m)
print(a,b,c,d)
print(e,f)
#RSI เกิน ให้ดูวันก่อนหน้าถ้าน้อยกว่า ให้ซื้อ 
#ขายเอาRIS เป็นหลัก ไม่เอา vol
