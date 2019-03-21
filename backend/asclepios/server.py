from keras import Sequential
from keras.layers import CuDNNLSTM, Dense
from lib.mqtt import Client
import random
import json
import time
import numpy as np
import pickle as pkl

from sklearn import linear_model
from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

def make_model():
    input_shape = (1, 1024)
    output_dim = 4 + 1
    model = Sequential()
    model.add(CuDNNLSTM(64, input_shape=input_shape, batch_size=None, return_sequences=False))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model

mqttc = Client()
with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())["development"]
    print(" * Config:", config)
mqttc.connect(config['broker_uri'], port=1883, keepalive=60)
mqttc.loop_start()



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

model = pkl.load(open('../../data/sklearn_model_fitted.pkl', 'rb'))
diseases = ['Myocardial infarction', 'Bundle branch block', 'Cardiomyopathy', 'twa']

last_preds = {
    disease: [] for disease in diseases
}

def get_score_health(pred):
    return pred['Healthy control'] * 100


def get_disease(pred, threshold=0.5):
    for disease in diseases:
        if pred[disease] > threshold:
            return disease
    return 'No disease clearly detected'


def notice_trends(last_preds, preds, n_last_elts_chosen=10):
    for disease in diseases:
        last_preds[disease].append(preds[disease])
    tendencies = []
    for disease in diseases:
        tendencies.append(linear_model.LinearRegression().fit(
            [i for i in range(n_last_elts_chosen)],
            [pred for pred in last_preds[disease][-n_last_elts_chosen:]]
        ).coef_[1])
    return dict(zip(diseases, tendencies))


def make_preds(d):
    r = {}
    for p in d.keys():
        if len(d[p]) == 1024:
            r[p] = d[p][0]["time"]
            X = np.array([[[d[p][i]["avg"] for i in range(1024)]]])
            return model.predict(X)
        else:
            r[p] = 0
            return None

while True:
    pred = make_preds(mqttc.storage.data)
    if pred!= None:
        print('score healthyness :', get_score_health(pred))
        print('disease detected', get_disease(pred))
        print('trends over probabilities', notice_trends(last_preds, pred))
        time.sleep(4)
