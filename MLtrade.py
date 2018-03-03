from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers
from keras import losses
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
    AvgLast = indi.AVGN(data=Last,day=5)
    AvgLast10 = indi.AVGN(data=Last,day=10)
    Chper = gf.getChPer(stock)
    Vol = gf.getVol(stock)
    MACD = indi.MACD(Last)
    RSI = indi.RSI(data=Last,day=14)
    AvgVol = indi.AVGN(data=Vol,day=5)
    AvgVol10 = indi.AVGN(data=Vol,day=10)
    # NomalZ = gf.Normaliz(data=Vol,avg= AvgVol)
    EMA5 = indi.EMA(data=Last,day=5)
    answer = []
    Last = list(filter(lambda a: a != None, Last))
    for x in range(0,len(Last)-1):
        rL = bs.findRange(Last[x+1],2)
        if Last[x] > rL[1]:
            answer.append(1)
        else:
            answer.append(0)
    answer.append(None)
    Elogic = [None]
    for x in range(0,len(Last)-1):
        buy = bs.buy(pLast=Last[x],nLast=Last[x+1],macd=MACD[x],avgVol=AvgVol[x],vol=Vol[x],nrsi=RSI[x+1],prsi=RSI[x])
        sell = bs.sell(pLast=Last[x],nLast=Last[x+1],avgVol=AvgVol[x],vol=Vol[x],ema=EMA5[x],pmacd=MACD[x],nmacd=MACD[x+1],nrsi=RSI[x+1],prsi=RSI[x])
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
            Elogic.append(0)
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

    for x in range(0,len(AvgLast10)):
        if(AvgLast10[x] == None):
            AvgLast10[x] = 0.01
    AvgLast10 = gf.flaot2deciamal(AvgLast10)
    
    for x in range(0,len(AvgLast)):
        if(AvgLast[x] == None):
            AvgLast[x] = 0.01
        AvgLast[x] = AvgLast[x]/((AvgLast10[x]+AvgLast[x]))
    AvgLast = gf.flaot2deciamal(AvgLast)

    for x in range(0,len(Last)):
        if(Last[x] == None):
            Last[x] = 0
        Last[x] = Last[x]/1000
        Last[x] = Last[x]/(1+Last[x])*10
    Last = gf.flaot2deciamal(Last)

    # for x in range(0,len(Elogic)):
    #     if(Elogic[x] == None):
    #         Elogic[x] = 0.1
    #     Elogic[x] = Elogic[x]/100
    # Elogic = gf.flaot2deciamal(Elogic)
    for x in range(0,len(AvgVol10)):
        if(AvgVol10[x] == None):
            AvgVol10[x] = 10000
    AvgVol10 = gf.flaot2deciamal(AvgVol10)

    for x in range(0,len(AvgVol)):
        if(AvgVol[x] == None):
            AvgVol[x] = 10000
        AvgVol[x] = AvgVol[x]/((AvgVol10[x]+AvgVol[x]))
    AvgVol = gf.flaot2deciamal(AvgVol)

    for x in range(0,len(Last)):
        if(RSI[x] == None or AvgVol[x] == None or MACD[x] == None or Elogic[x] == None or AvgLast[x] == None):
            continue
        temp.append(Chper[x])
        temp.append(Last[x])
        temp.append(RSI[x])
        temp.append(AvgVol[x])
        temp.append(MACD[x])
        temp.append(AvgLast[x])
        dim.append(temp)
        # print(temp)
        temp = []

    for x in range(0,len(answer)-len(dim)):
        answer.pop(0)
    answer.pop()
    dim.pop()
    # print(len(answer),len(dim))
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
model.add(Dense(125, activation='relu', input_dim=6))
model.add(Dense(200, activation='softmax'))
model.add(Dense(200, activation='softmax'))
model.add(Dense(1,activation = 'sigmoid'))
optimizer = optimizers.SGD(lr=0.02, momentum=0.0, decay=0.0, nesterov=False)
model.compile(optimizer=optimizer,
              loss='mean_squared_error',
              metrics=['accuracy'])

# model.compile(loss='mean_squared_error', optimizer='sgd',metrics=['accuracy'])
th = 600
start = 300
symbol = gf.allSymbol()
data,answer = diminput(symbol[start])
labels = answer
SRAnswer = answer
# print("\n",len(labels),len(data))
stop = 350
# print(answer)
for x in range(start+1,stop):
    sys.stdout.write("Download progress: %.2f%%   \r" % (100*(x-start)/(stop-start)) )
    sys.stdout.flush()
    try:
        dataT,answerT = diminput(symbol[x])
        if dataT == None or answerT == None:
            continue
        labelsT =  answerT
        # print("\n")
        data = connector(data,dataT)
        # print(len(labels),len(labelsT),"B")
        labels = connector(labels,labelsT)
        # print(len(labels),len(labelsT),"A")
        # SRAnswer = connector(SRAnswer,answerT)
        # print("\n",len(data),len(labels)," 321321321321 ")
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
# print(len(data),len(labels),"asasdasd")
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


model.fit(data,labels,epochs=200,batch_size=700)
# model.save_weights(fname,overwrite=True)



# for x in range(0,20):
#     print(d[x],l[x])
k1 = 400
k2 = 420

for x in range(k1,k2):
    print(data[x],labels[x])
# model.load_weights(fname)



k = [data[x] for x in range(k1,k2)]
p = model.predict(k)
print(p)
for y in range(0,len(p)):
    if p[y] > 0.5:
        print("Interest")
    else:
        print("Nope")


# for x in range(0,len())