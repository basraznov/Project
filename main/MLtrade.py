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

AllFeature = 6

def diminput(Symbol):
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
            answer.append(1)
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
    ######################################################################### old
    # for x in range(0,len(Chper)):
    #     if(Chper[x] == None):
    #         Chper[x] = 0
    #     else:
    #         Chper[x] = Chper[x]/10
    # Chper = gf.flaot2deciamal(Chper)

    # for x in range(0,len(RSI)):
    #     if(RSI[x] == None):
    #         RSI[x] = 0
    #     RSI[x] = RSI[x]/100
    # RSI = gf.flaot2deciamal(RSI)

    # for x in range(0,len(AvgLast10)):
    #     if(AvgLast10[x] == None):
    #         AvgLast10[x] = 0.01
    # AvgLast10 = gf.flaot2deciamal(AvgLast10)
    
    # for x in range(0,len(AvgLast)):
    #     if(AvgLast[x] == None):
    #         AvgLast[x] = 0
    #     if x != 0:
    #         AvgLast[x] = AvgLast[x]/(AvgLast10[x-1])
    #     else:
    #         AvgLast[x] = 0
    # AvgLast = gf.flaot2deciamal(AvgLast)

    # # for x in range(0,len(Elogic)):
    # #     if(Elogic[x] == None):
    # #         Elogic[x] = 0.1
    # #     Elogic[x] = Elogic[x]/100
    # # Elogic = gf.flaot2deciamal(Elogic)

    # for x in range(0,len(AvgVol10)):
    #     if(AvgVol10[x] == None):
    #         AvgVol10[x] = 10000
    # AvgVol10 = gf.flaot2deciamal(AvgVol10)

    # for x in range(0,len(AvgVol)):
    #     if(AvgVol[x] == None):
    #         AvgVol[x] = 0
    #     if x != 0:
    #         AvgVol[x] = AvgVol[x]/(AvgVol10[x-1])
    #     else:
    #         AvgVol[x] = 0
    # AvgVol = gf.flaot2deciamal(AvgVol)

    # for x in range(0,len(Vol)):
    #     if(Vol[x] == None):
    #         Vol[x] = 0
    # Vol = gf.flaot2deciamal(Vol)

    # for x in range(0,len(Last)):
    #     if(Last[x] == None):
    #         Last[x] = 0
    # TLast = gf.flaot2deciamal(Last)

    # for x in range(0,len(Last)):
    #     if(Last[x] == None):
    #         Last[x] = 0
    #     if(x != 0):
    #         Last[x] = (Last[x]-AvgLast10[x-1])/AvgLast10[x-1]
    #     else:
    #         Last[x] = 0
    # Last = gf.flaot2deciamal(Last)
    ############################################### old
    ############################################### new
    for x in range(0,len(Chper)):
        if(Chper[x] == None):
            Chper[x] = 0
        elif Chper[x] > 0:
            Chper[x] = 0
        else:
            Chper[x] = 1
    # Chper = gf.flaot2deciamal(Chper)
    
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


    # for x in range(0,len(AvgLast)):
    #     if(AvgLast[x] == None):
    #         AvgLast[x] = 0
    #     if x != 0:
    #         AvgLast[x] = AvgLast[x]/(AvgLast10[x-1])
    #     else:
    #         AvgLast[x] = 0
    # AvgLast = gf.flaot2deciamal(AvgLast)

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

    # for x in range(0,len(Vol)):
    #     if(Vol[x] == None):
    #         Vol[x] = 0
    # Vol = gf.flaot2deciamal(Vol)

    # for x in range(0,len(Last)):
    #     if(Last[x] == None):
    #         Last[x] = 0
    # TLast = gf.flaot2deciamal(Last)

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
    # print(len(RSIM),len(RSI70),len(RSI30),len(AvgVolM),len(Last10Avg))
    #########Z##################################### new

    for x in range(0,len(Last)):
        # if(RSI[x] == None or AvgVol[x] == None or MACD[x] == None or Elogic[x] == None or AvgLast[x] == None):
        #     continue
        ########################################################## old
        # temp.append(Chper[x])
        # temp.append(TLast[x])
        # temp.append(Last[x]) # (ราคาปัญจุบัน - ราคาเฉลีย)/ราคาเฉลีย # 5% 10%
        # temp.append(RSI[x]) #เพิ่มขึ้นหรือลดลง มากกว่า
        # temp.append(AvgVol[x]) # แก้ vol/volavg 10 # 100%
        # temp.append(MACD[x]) # แก้ macdปัจุบัน / macdเฉลีย10วัน #เพิ่มขึ้นหรือลดลง
        # temp.append(AvgLast[x]) #ไม่ต้อง
        # temp.append(Elogic[x])
        ######################################################### old
        ######################################################### new
        temp.append(RSIM[x])
        temp.append(RSI70[x])
        temp.append(RSI30[x])
        temp.append(AvgVolM[x])
        temp.append(Last10Avg[x])
        temp.append(Elogic[x])
        # temp.append()
        # temp.append()
        dim.append(temp)
        # print(temp)
        temp = []
        #Chper,Last,(Last-AvgLast)/AvgLast,RSI,Vol/AvgVol,MACD,Last/AvgLast

    for x in range(0,len(answer)-len(dim)):
        answer.pop(0)
    answer.pop()
    dim.pop()


    # testanswer = []
    # for x in range(0,len(dim)):
    #     if AvgVolM[x] == 1 and Last10Avg[x] == 1:
    #         testanswer.append(1)
    #     else:
    #         testanswer.append(0)
        # print(AvgVolM[x],dim[x][0],"||",Last10Avg[x],dim[x][1],"||",testanswer[x])
    
    # print(len(testanswer),len(dim),len(answer))

    # print(len(answer),len(dim),Symbol)
    # for x in range(0,len(dim)): 
    #     if (answer[x] == 1):
    #         print(x,dim[x],answer[x])
    # return dim,testanswer
    return dim,answer

def connector(data1,data2):
    for x in range(0,len(data2)):
        data1.append(data2[x])
    return data1

def tranfromAnswer(answer):
    tmp = []
    for x in range(0,len(answer)):
        if answer[x] == 1:
            tmp.append([1,0])
        if answer[x] == 0:
            tmp.append([0,1])
    return tmp

model = Sequential()
model.add(Dense(20, activation='relu', input_dim=AllFeature))
model.add(Dense(150, activation='relu'))
model.add(Dense(80, activation='relu'))
model.add(Dense(1,activation = 'sigmoid'))
optimizer = optimizers.SGD(lr=2, momentum=0.00, decay=0, nesterov=False)
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
goodStock = ["CBG"]
goodStock = ["CBG","ASIAN","GFPT","STA","AH","SAT","KBANK","TMB","KTB","SCB","BBL","BAY"]
# goodStock = ["CBG","ASIAN","GFPT","STA","AH","SAT","KBANK","TMB","KTB","SCB","BBL","BAY","CPALL","BEAUTY","HMPRO","BJC","SCC","TOA","TASCO","TPIPL","KCE","HANA","DELTA","SMT","CCET","PTT","BANPU","PTTEP","IRPC","TOP","ESSO","MTLS","SAWAD","KTC","AEONTS","CPF","MINT","M","TU","MALEE","TVO","TIPCO","BDMS","BH","BCH","CHG","SNC","TRUE","ADVANC","DTAC","INTUCH","JAS","SAMART","TIP","BLA","AYUD","BEC","WORK","RS","VGI","MAJOR","EA","FSMART","MONO","PTL","AJ","UTP","IVL","PTTGC","GGC","VNT","AMATA","CPN","LH","STEC","WHA","UNIQ","CK","CENTEL","ERW","AOT","BTS","PSL","THAI","TTA","AAV"]

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

# with open("DataForML.txt", 'a') as out:
#     for y in range(len(data)):
#         for x in range(len(data[y])):
#             out.write(str(data[y][x])+',')
#         out.write(str(labels[y])+'\n')
# print(data[1])
ln = 1
data = np.array(data)
Tlabels = tranfromAnswer(labels)
Tlabels = np.array(Tlabels)
labels = np.array(labels)
labels = np.reshape(labels,(len(labels),1))
# dl = np.concatenate((data, Tlabels), axis=1)
dl = np.concatenate((data, labels), axis=1)
dl1 = np.zeros([0,AllFeature+ln], dtype=float)
dl0 = np.zeros([0,AllFeature+ln], dtype=float)
# print (dl1.shape,dl0.shape,dl.shape)
for x in range(len(dl)):
    sys.stdout.write("Calculate progress: %.2f%%   \r" % (100*(x)/(len(dl)))  )
    sys.stdout.flush()
    if dl[x][-ln] == 0:
        dl0 = np.append(dl0, np.reshape(dl[x],(1,AllFeature+ln)), axis=0)
    if dl[x][-ln] == 1:
        dl1 = np.append(dl1, np.reshape(dl[x],(1,AllFeature+ln)), axis=0)
print()

randl0 = np.zeros([0,AllFeature+1], dtype=float)
count = 0
randl0 = dl0
while len(randl0) != len(dl1)*1:
    sys.stdout.write("Calculate true progress: %.2f%%   \r" % (100*(x)/(len(dl)))  )
    sys.stdout.flush()
    ran = np.random.randint(len(dl0)-count, size=1)[0]
    randl0 = np.delete(randl0, ran, 0)
    # randl0 = np.append(dl0, np.reshape(dl0[ran],(1,AllFeature+1)), axis=0)
    count += 1
print()
alldl = np.concatenate((randl0, dl1), axis=0)
np.random.shuffle(alldl)
# separater = int(len(alldl)*0.8)
separater = len(alldl)-250
data = alldl[:separater,:AllFeature]
labels = alldl[:separater,AllFeature:]
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
# for x in range(len(data)):
#     if data[x][0] == 1 and data[x][0] == 1 and labels[x] == 1:
#         print(data[x],labels[x],1)
#     else:
#         print(data[x],labels[x],0)

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
# for x in range(len(data)):
#     print(data[x])
# print(labels)
################################################################# train and predict
print(data.shape,labels.shape)
model.fit(data,labels,epochs=80,batch_size=20)
model.save_weights(fname,overwrite=True)

preData = alldl[separater:,:AllFeature]
preLabels = alldl[separater:,AllFeature:]
print(preData)
print(preLabels)

p = model.predict(preData)
print("---------------------------------")
print(p)
correct = 0
for y in range(0,len(p)):
    if p[y] > 0.5:
        print("Interest")
    else:
        print("Nope")
    if p[y] > 0.5 and preLabels[y] == 1:
        correct += 1
    elif p[y] < 0.5 and preLabels[y] == 0:
        correct += 1
print(correct/len(p)*100)

# for x in range(0,len())
#################################################################



#ให้จาร ข้อมูลที่ไปlearn