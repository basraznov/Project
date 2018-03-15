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
import random

fname = "Save.hdf5"
a = 0
b = 0
c = 0
d = 0
e = 0
f = 0
xxx = 0
xxy = 0
xxz = 0

AllFeature = 4
NumFeature = 7

def diminput(Symbol):
    global a
    global b
    global c
    global d
    global e
    global f
    global xxx
    global xxy
    global xxz
    global AllFeature

    stock = gf.getData(Symbol)
    if len(stock) < 60:
        return None,None
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
    # print(len(Last),len(AvgLast),len(AvgLast10),len(Chper),len(Vol),len(MACD),len(MACDAvg10),len(RSI),len(AvgVol),len(AvgVol10))
    answer = []
    for x in range(0,len(Last)-1):
        # rL = bs.findRange(Last[x+1],2)
        # if Last[x] < rL[0]:
        #     answer.append(1)
        # else:
        #     answer.append(0)
        if x == 0 or Last[x] == None or AvgLast10[x-1] == None or Vol[x] == None or AvgVol10[x-1] == None:
            answer.append(0)
            continue
        if Last[x] > AvgLast10[x-1] and Vol[x] > AvgVol10[x-1]*2:
            answer.append(2)
        else:
            answer.append(0)
    Last = list(filter(lambda a: a != None, Last))
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
        RSI[x] = RSI[x]/100
    RSI = gf.flaot2deciamal(RSI)

    for x in range(0,len(AvgLast10)):
        if(AvgLast10[x] == None):
            AvgLast10[x] = 0.01
    AvgLast10 = gf.flaot2deciamal(AvgLast10)
    
    for x in range(0,len(AvgLast)):
        if(AvgLast[x] == None):
            AvgLast[x] = 0
        if x != 0:
            AvgLast[x] = AvgLast[x]/(AvgLast10[x-1])
        else:
            AvgLast[x] = 0
    AvgLast = gf.flaot2deciamal(AvgLast)

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
            AvgVol[x] = 0
        if x != 0:
            AvgVol[x] = AvgVol[x]/(AvgVol10[x-1])
        else:
            AvgVol[x] = 0
    AvgVol = gf.flaot2deciamal(AvgVol)

    for x in range(0,len(Vol)):
        if(Vol[x] == None):
            Vol[x] = 0
    Vol = gf.flaot2deciamal(Vol)

    for x in range(0,len(Last)):
        if(Last[x] == None):
            Last[x] = 0
    TLast = gf.flaot2deciamal(Last)

    for x in range(0,len(Last)):
        if(Last[x] == None):
            Last[x] = 0
        if(x != 0):
            Last[x] = (Last[x]-AvgLast10[x-1])/AvgLast10[x-1]
        else:
            Last[x] = 0
    Last = gf.flaot2deciamal(Last)

    for x in range(0,len(Last)):
        if(RSI[x] == None or AvgVol[x] == None or MACD[x] == None or Elogic[x] == None or AvgLast[x] == None):
            continue
        temp.append(Chper[x])
        # temp.append(TLast[x])
        temp.append(Last[x]) # (ราคาปัญจุบัน - ราคาเฉลีย)/ราคาเฉลีย # 5% 10%
        # temp.append(RSI[x]) #เพิ่มขึ้นหรือลดลง มากกว่า
        temp.append(AvgVol[x]) # แก้ vol/volavg 10 # 100%
        # temp.append(MACD[x]) # แก้ macdปัจุบัน / macdเฉลีย10วัน #เพิ่มขึ้นหรือลดลง
        temp.append(AvgLast[x]) #ไม่ต้อง
        # temp.append(Elogic[x])
        dim.append(temp)
        # print(temp)
        temp = []
    

    for x in range(0,len(answer)-len(dim)):
        answer.pop(0)
    answer.pop()
    dim.pop()
    # print(len(answer),len(dim),Symbol)
    # for x in range(0,len(dim)): 
    #     if (answer[x] == 1):
    #         print(x,dim[x],answer[x])
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
model.add(Dense(200, activation='softmax', input_dim=AllFeature))
model.add(Dense(500, activation='softmax'))
model.add(Dense(1,activation = 'sigmoid'))
optimizer = optimizers.SGD(lr=0.125, momentum=0.00, decay=0, nesterov=False)
model.compile(optimizer=optimizer,
            loss='mean_squared_error',
            metrics=['accuracy'])

# model.compile(loss='mean_squared_error', optimizer='sgd',metrics=['accuracy'])
# ######################################################################### old 
# start = 300
# symbol = gf.allSymbol()
# th = symbol.index("PTT")
# # stock 
# data,answer = diminput(symbol[th])
# labels = answer
# SRAnswer = answer
# # print("\n",len(labels),len(data))
# stop = 300
# # print(answer)
# for x in range(start+1,stop):
#     sys.stdout.write("Download progress: %.2f%%   \r" % (100*(x-start)/(stop-start)) )
#     sys.stdout.flush()
#     try:
#         dataT,answerT = diminput(symbol[x])
#         if dataT == None or answerT == None:
#             continue
#         labelsT =  answerT
#         # print("\n")
#         data = connector(data,dataT)
#         # print(len(labels),len(labelsT),"B")
#         labels = connector(labels,labelsT)
#         # print(len(labels),len(labelsT),"A")
#         # SRAnswer = connector(SRAnswer,answerT)
#         # print("\n",len(data),len(labels)," 321321321321 ")
#     except Exception as e:
#         print("Error in "+str(x)+" symbol is "+symbol[x])
#         traceback.print_exc()
#         exit()
# print()
# k = 0
# j = 0
# l = 0
# m = 0
# p = 1
# ############################################################################


############################################################################## new
symbol = gf.allSymbol()
data = []
labels = []
k = 0
# goodStock = ["PTT","BANPU"]
goodStock = ["PTT","BANPU","EA","CPF","MINT","PTTGC","IVL","TPIPL","SCC","CPALL","BEAUTY","AOT","BEM","ADVANC","TRUE","KBANK","SCB","KTC","MTLS","AMATA","CPN","VGI","RS","CBG","GFPT","CWT","AH"]
# goodStock = ["PTT","BANPU","EA","CPF","MINT","PTTGC","IVL","TPIPL","SCC","CPALL","BEAUTY","AOT","BEM","ADVANC","TRUE","KBANK","SCB","KTC","MTLS","AMATA","CPN","VGI","RS","CBG","GFPT","CWT","AH","HANA","KCE","SUC","AYUD","PTL","DDD","B-WORK","WHART","THE","TMT","ERW","CENTEL"]
for x in range(len(goodStock)):
    sys.stdout.write("Download progress: %.2f%%   \r" % (100*(x)/(len(goodStock))) )
    sys.stdout.flush()
    try:
        dataT,answerT = diminput(goodStock[x])
        if dataT == None or answerT == None:
            continue
        labelsT =  answerT
        data = connector(data,dataT)
        labels = connector(labels,labelsT)
    except Exception as e:
        print("Error in "+str(x)+" symbol is "+symbol[x])
        traceback.print_exc()
        exit()
print("Download progress: 100.00")
data = np.array(data)
labels = np.array(labels)
labels = np.reshape(labels,(len(labels),1))
dl = np.concatenate((data, labels), axis=1)
dl1 = np.zeros([0,AllFeature+1], dtype=float)
dl0 = np.zeros([0,AllFeature+1], dtype=float)
for x in range(len(dl)):
    if dl[x][-1] == 0:
        dl0 = np.append(dl0, np.reshape(dl[x],(1,AllFeature+1)), axis=0)
    if dl[x][-1] == 2:
        dl1 = np.append(dl1, np.reshape(dl[x],(1,AllFeature+1)), axis=0)
print (dl1.shape,dl0.shape)
randl0 = np.zeros([0,AllFeature+1], dtype=float)
count = 0
randl0 = dl0
while len(randl0) != len(dl1)*1:
    ran = np.random.randint(len(dl0)-count, size=1)[0]
    randl0 = np.delete(randl0, ran, 0)
    # randl0 = np.append(dl0, np.reshape(dl0[ran],(1,AllFeature+1)), axis=0)
    count += 1
alldl = np.concatenate((randl0, dl1), axis=0)
np.random.shuffle(alldl)
# separater = int(len(alldl)*0.8)
separater = len(alldl)-10
data = alldl[:separater,:AllFeature]
labels = alldl[0:separater,AllFeature:]
print(data)
# print (temp)
############################################################################## 

############################################################################## check anwser
# print(len(data),len(labels),"asasdasd")
# for x in range(0,len(data)-1):
    # if (data[x][4])*100 == answer[x]:
    #     k+=1
    # if answer[x] == 1:
    #     l+=1
    # if answer[x] == 0:
    #     j+=1
    # if answer[x] == -1:
    #     m+=1
    # p += 1
# print(k,len(data),k/len(data),xxx,xxy,xxz)
# print(l,j,m)
# print(a,b,c,d)
# print(e,f)
##############################################################################

############################################################################## test new style
# cY = 0
# cN = 0
# mm = 0
# newdataY = []
# newanswerY = []
# newdataN = []
# newanswerN = []
# print(len(data),len(answer))
# for x in range(len(data)):
#     if answer[x] == 1:
#         cY += 1
#         newdataY.append(data[x])
#         newanswerY.append(answer[x])
#     else:
#         cN += 1
#         newdataN.append(data[x])
#         newanswerN.append(answer[x])

# while len(newanswerN) > len(newanswerY)*1.5:
#     k = random.randint(0, len(newanswerN)-1)
#     newanswerN.pop(k)
#     newdataN.pop(k)
#     mm += 1

# print(len(newdataY),len(newanswerY),cY)
# print(len(newdataN),len(newanswerN),mm)

# for x in range(len(newanswerN)):
#     newdataY.append(newdataN[x])
#     newanswerY.append(newanswerN[x])

# model.fit(newdataN,newanswerN,epochs=200,batch_size=700)
# model.save_weights(fname,overwrite=True)

# k1 = 400
# k2 = 420
# print ("----")
# data = np.array(data)
# xx = data[:len(data),:6].tolist()
# yy = data[:len(data),6:].tolist()
# model.fit(xx,yy,epochs=200,batch_size=700)
# aa = data[k1:k2,:6]
# p = model.predict(aa)
# print(p)
# for y in range(0,len(p)):
#     if p[y] > 0.3:
#         print("Interest")
#     else:
#         print("Nope")


# for x in range(0,20):
#     print(d[x],l[x])


##############################################################################
# model.load_weights(fname)

# print(labels)
################################################################# train and predict
model.fit(data,labels,epochs=200,batch_size=100)

preData = alldl[separater:,:AllFeature]
preLabels = alldl[separater:,AllFeature:]
print(preData)
print(preLabels)

# k = [data[x] for x in range(k1,k2)]
p = model.predict(preData)
print("---------------------------------")
print(p)

for y in range(0,len(p)):
    if p[y] > 0.5:
        print("Interest")
    else:
        print("Nope")


# for x in range(0,len())
#################################################################



#ให้จาร ข้อมูลที่ไปlearn