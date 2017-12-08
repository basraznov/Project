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
    EMA12 = indi.EMA(data=Last,day=12)
    answer = []
    for x in range(0,len(Last)-1):
        if Last[x] > Last[x+1]:
            answer.append(-1)
        elif Last[x] < Last[x+1]:
            answer.append(1)
        else:
            answer.append(0)
    answer.append(None)
    dim = []
    dim.append(Chper)
    dim.append(RSI)
    dim.append(NomalZ)
    dim.append(MACD)
    print(dim[0][0],dim[1][0],dim[2][0],dim[3][0])
    print(len(EMA12),len(Chper),len(MACD),len(RSI),len(NomalZ))    
    # print(len(Last),len(Vol),len(RSI),len(answer),len(NomalZ),len(MACD))


model = Sequential()
model.add(Dense(35, activation='relu', input_dim=2))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

diminput("AAV")


# model.fit(data,labels,epochs=1,batch_size=100)

# fname = "plusSave.hdf5"
# model.save_weights(fname,overwrite=True)
# model.load_weights(fname)
# p = model.predict([[2,3],[4,5],[1,3],[9,6],[8,9],[8,6],[7,4]])
# for x in p:
#     print(np.argmax(x))

