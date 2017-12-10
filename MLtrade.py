from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np
import indicator as indi
import getandformat as gf
import buyorsell as bs

def diminput(Symblo):
    stock = gf.getData(Symblo)
    Last = gf.getLast(stock)
    Chper = gf.getChPer(stock)
    Vol = gf.getVol(stock)
    MACD = indi.MACD(Last)
    RSI = indi.RSI(data=Last,day=14)
    AvgVol = indi.AVG(Vol)
    NomalZ = gf.Normaliz(data=Vol,avg= AvgVol)
    EMA5 = indi.EMA(data=Last,day=5)
    answer = []
    for x in range(0,len(Last)-1):
        if Last[x] > Last[x+1]:
            answer.append(-1)
        elif Last[x] < Last[x+1]:
            answer.append(1)
        else:
            answer.append(0)
    answer.append(None)
    Elogic = [None]
    for x in range(1,len(Last)):
        buy = bs.buy(pLast=Last[x-1],nLast=Last[x],macd=MACD[x],rsi=RSI[x],avgVol=AvgVol,vol=Vol[x])
        sell = bs.sell(pLast=Last[x-1],nLast=Last[x],avgVol=AvgVol,vol=Vol[x],ema=EMA5[x])
        if buy == None or sell == None:
            Elogic.append(None)
        elif buy == False and sell == False:
            Elogic.append(0)
        elif buy == True and sell == False:
            Elogic.append(1)
        elif buy == False and sell == True:
            Elogic.append(-1)
        else:
            Elogic.append(9)
    dim = []
    temp = []
    for x in range(0,len(Last)):
        if(Chper[x] == None):
            Chper[x] = 0
        if(RSI[x] == None or NomalZ[x] == None or MACD[x] == None or Elogic[x] == None):
            continue
        temp.append(Chper[x]/100)
        temp.append(RSI[x]/100)
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
        print(x,dim[x],answer[x])
    return answer,dim



def connector(data1,data2):
    for x in range(0,len(data2)):
        data1.append(data2[x])
    return data1



model = Sequential()
model.add(Dense(35, activation='relu', input_dim=2))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

temp = diminput("AAV")
data = temp.dim
answer = temp.answer


# model.fit(data,labels,epochs=1,batch_size=100)

# fname = "plusSave.hdf5"
# model.save_weights(fname,overwrite=True)
# model.load_weights(fname)
# p = model.predict([[2,3],[4,5],[1,3],[9,6],[8,9],[8,6],[7,4]])
# for x in p:
#     print(np.argmax(x))

