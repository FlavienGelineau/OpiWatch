from keras import Sequential
from keras.layers import CuDNNLSTM, Dense
import numpy as np
import pickle as pkl

def make_model():
    input_shape = (1, 1024)
    output_dim = 4
    model = Sequential()
    model.add(CuDNNLSTM(64, input_shape=input_shape, batch_size=None, return_sequences=False))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    model.load_weights('weights_best_model')

    return model

model = pkl.load(open('sklearn_model_fitted.pkl', 'rb'))

pred = np.array([[
    [0.2 for _ in range(1024)]
]])
print(pred.shape)

print(pred)
import time
start = time.time()
print(model.predict_proba(pred))
print(time.time() - start)