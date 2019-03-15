from keras import Sequential
from keras.layers import CuDNNLSTM, Dense
import numpy as np

def make_model(input_shape, output_dim):
    model = Sequential()
    model.add(CuDNNLSTM(64, input_shape=input_shape, batch_size=None, return_sequences=False))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model

model = make_model((1, 1024), 4)
model.load_weights('weights_best_model')

pred = np.array([[
    [0.2 for _ in range(1024)]
    ]
])
print(pred.shape)

print(pred)

print(model.predict(pred))