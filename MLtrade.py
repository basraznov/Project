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


trade = gf.getLast(gf.getData("AAV"))
EMA5 = indi.EMA(data=trade,day=5)
EMA10 = indi.EMA(data=trade,day=10)
print(EMA5)

# model.fit(data,labels,epochs=1,batch_size=100)

# fname = "plusSave.hdf5"
# model.save_weights(fname,overwrite=True)
# model.load_weights(fname)
# p = model.predict([[2,3],[4,5],[1,3],[9,6],[8,9],[8,6],[7,4]])
# for x in p:
#     print(np.argmax(x))

