import pandas as pd
from keras.layers import CuDNNLSTM
from keras.layers import Dense
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.metrics import confusion_matrix, classification_report
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from classification.data_managing import get_rnn_train_test_set

from sklearn.pipeline import make_pipeline
import numpy as np
from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler

import pickle as pkl


def make_model():
    input_shape = (1, 1024)
    output_dim = 4+1
    model = Sequential()
    model.add(CuDNNLSTM(64, input_shape=input_shape, batch_size=None, return_sequences=False))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model


class NDStandardScaler(TransformerMixin):
    def __init__(self, **kwargs):
        self._scaler = StandardScaler(copy=True, **kwargs)
        self._orig_shape = None

    def fit(self, X, y, **kwargs):
        X = np.array(X)
        # Save the original shape to reshape the flattened X later
        # back to its original shape
        if len(X.shape) > 1:
            self._orig_shape = X.shape[1:]
        X = self._flatten(X)
        self._scaler.fit(X, **kwargs)
        return self

    def transform(self, X, **kwargs):
        X = np.array(X)
        X = self._flatten(X)
        X = self._scaler.transform(X, **kwargs)
        X = self._reshape(X)
        return X

    def _flatten(self, X):
        # Reshape X to <= 2 dimensions
        if len(X.shape) > 2:
            n_dims = np.prod(self._orig_shape)
            X = X.reshape(-1, n_dims)
        return X

    def _reshape(self, X):
        # Reshape X back to it's original shape
        if len(X.shape) >= 2:
            X = X.reshape(-1, *self._orig_shape)
        return X


selected_labels = ['Healthy control', 'Myocardial infarction', 'Bundle branch block', 'Cardiomyopathy', 'twa']
window_size = 1024

load_precedents = False
if load_precedents:
    trainX, trainY, testX, testY, record_list = pkl.load(open('../data/cached_data.pkl', 'rb'))
else:
    trainX, trainY, testX, testY, record_list = get_rnn_train_test_set(selected_labels, window_size)
    pkl.dump((trainX, trainY, testX, testY, record_list), open('../.data/cached_data.pkl', 'wb'))

checkpoint = ModelCheckpoint('../data/weights_best_model', monitor='val_loss', verbose=1, save_best_only=True, mode='min')
early_stopping = EarlyStopping(patience=5)
callbacks_list = [checkpoint, early_stopping]

model = KerasClassifier(make_model,
                        validation_split=0.15,
                        epochs=100,
                        batch_size=512,
                        callbacks=callbacks_list,
                        verbose=0)
scaler = NDStandardScaler()

model = make_pipeline(scaler, model)
model.fit(trainX, trainY)
import pickle as pkl

pkl.dump(model, open('../data/sklearn_model_fitted.pkl', 'wb'))
print(testX.shape)
output = model.predict_proba(testX)
print(len(record_list), len(output), len(testY.argmax(axis=1)))
print(testY.argmax(axis=1))
print(output.argmax(axis=1))
summed = pd.DataFrame({'record': record_list,
                       'predictions': output.argmax(axis=1),
                       'label': testY.argmax(axis=1)})
summed = summed.groupby('record').mean()
summed["predicted label"] = summed['predictions'] > 0.5

print(confusion_matrix(testY.argmax(axis=1), output.argmax(axis=1)))
print(classification_report(summed['label'], summed["predicted label"]))
