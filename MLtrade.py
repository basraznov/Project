from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np
import indicator as indi
import getandformat as gf


model = Sequential()
model.add(Dense(35, activation='relu', input_dim=2))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])


stock = gf.getData("AAV")
Last = gf.getLast(stock)
Chper = gf.getChPer(stock)
Vol = gf.getVol(stock)
MACD = indi.MACD(Last)
RSI = indi.RSI(data=Last,day=14)
AvgVol = indi.AVG(Vol)
NomalZ = gf.Normaliz(data=Vol,avg= AvgVol)
answer = []
for x in range(0,len(Last)-1):
    if Last[x] > Last[x+1]:
        answer.append(-1)
    elif Last[x] < Last[x+1]:
        answer.append(1)
    else:
        answer.append(0)
answer.append(None)
print(len(Last),len(Vol),len(RSI),len(answer),len(NomalZ))
# model.fit(data,labels,epochs=1,batch_size=100)

# fname = "plusSave.hdf5"
# model.save_weights(fname,overwrite=True)
# model.load_weights(fname)
# p = model.predict([[2,3],[4,5],[1,3],[9,6],[8,9],[8,6],[7,4]])
# for x in p:
#     print(np.argmax(x))
