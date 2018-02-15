from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np
import indicator as indi
import format as gf
import buyorsell as bs
import sys
import traceback

fname = "Save.hdf5"
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
    answer = []
    Last = list(filter(lambda a: a != None, Last))
    for x in range(0,len(Last)-1):
        rL = bs.findRange(Last[x+1],2)
        if Last[x] > rL[1]:
            answer.append(-1)
        elif Last[x] < rL[0]:
            answer.append(1)
        else:
            answer.append(0)
    answer.append(None)
    Elogic = [None]
    for x in range(0,len(Last)-1):
        buy = bs.buy(pLast=Last[x],nLast=Last[x+1],macd=MACD[x],avgVol=AvgVol,vol=Vol[x],nrsi=RSI[x+1],prsi=RSI[x])
        sell = bs.sell(pLast=Last[x],nLast=Last[x+1],avgVol=AvgVol,vol=Vol[x],ema=EMA5[x],pmacd=MACD[x],nmacd=MACD[x+1],nrsi=RSI[x+1],prsi=RSI[x])
        if buy == None or sell == None:
            Elogic.append(None)
        elif buy == False and sell == False:
            a += 1
            Elogic.append(0)
        elif buy == True and sell == False:
            b += 1
            Elogic.append(1)
        elif buy == False and sell == True:
            c += 1
            Elogic.append(-1)
        elif buy == True and sell == True:
            d += 1
            Elogic.append(0)
        else:
            Elogic.append(9)
        if buy == True:
            e += 1
        if sell == True:
            f += 1
    dim = []
    temp = []
    for x in range(0,len(Chper)):
        if(Chper[x] == None):
            Chper[x] = 0
        else:
            Chper[x] = Chper[x]/10
    Chper = gf.flaot2deciamal(Chper)

    for x in range(0,len(RSI)):
        if(RSI[x] == None):
            RSI[x] = 0
        RSI[x] = RSI[x]/1000
    RSI = gf.flaot2deciamal(RSI)

    for x in range(0,len(Elogic)):
        if(Elogic[x] == None):
            Elogic[x] = 1
        Elogic[x] = Elogic[x]/100
    Elogic = gf.flaot2deciamal(Elogic)

    for x in range(0,len(Last)):
        if(RSI[x] == None or NomalZ[x] == None or MACD[x] == None or Elogic[x] == None):
            continue
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
    # for x in range(0,len(dim)):
    #     print(x,dim[x],answer[x])
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

model = Sequential()
model.add(Dense(5, activation='relu', input_dim=5))
model.add(Dense(60, activation='relu'))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy'     ,
              metrics=['accuracy'])

# model.compile(loss='mean_squared_error', optimizer='sgd',metrics=['accuracy'])
th = 350
start = 200
symbol = gf.allSymbol()
data,answer = diminput(symbol[start])
labels = tranfromAnswer(answer)
SRAnswer = answer
stop = 200
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
    if (data[x][4])*100 == answer[x]:
        k+=1
    if answer[x] == 1:
        l+=1
    if answer[x] == 0:
        j+=1
    if answer[x] == -1:
        m+=1
    p += 1
print(k,len(data),k/len(data))
# print(l,j,m)
# print(a,b,c,d)
# print(e,f)



d = []
l = []
for x in range(0,20):
    l.append(labels[x])
    d.append(data[x])


model.fit(data,labels,epochs=20000,batch_size=700)
# model.save_weights(fname,overwrite=True)



# for x in range(0,20):
#     print(d[x],l[x])


# for x in range(0,10):
#     print(data[x],labels[x])
# model.load_weights(fname)
# p = model.predict([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]])
# print(p)
# for y in range(0,len(p)):
#     if p[y][0] > p[y][1] and p[y][0] > p[y][2]:
#         print("[1,0,0]")
#     elif p[y][1] > p[y][0] and p[y][1] > p[y][2]:
#         print("[0,1,0]")
#     elif p[y][2] > p[y][1] and p[y][2] > p[y][0]:
#         print("[0,0,1]")
#     else:
#         print("wrong")


# for x in range(0,len())