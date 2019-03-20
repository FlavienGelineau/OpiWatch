from lib.mqtt import Client
import random
import json
import time
import numpy as np
import pickle as pkl

from sklearn import linear_model

mqttc = Client()
with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())["development"]
    print(" * Config:", config)
mqttc.connect(config['broker_uri'], port=1883, keepalive=60)
mqttc.loop_start()

model = pkl.load(open('sklearn_model_fitted.pkl', 'rb'))
diseases = ['Myocardial infarction', 'Bundle branch block', 'Cardiomyopathy', 'twa']

last_preds = {
disease:[] for disease in diseases
}

def get_score_health(pred):
    return pred['Healthy control']*100

def get_disease(pred, threshold = 0.5):
    for disease in diseases:
        if pred[disease]>threshold:
            return disease
    return 'No disease clearly detected'

def notice_trends(last_preds, preds, n_last_elts_chosen = 10):

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
        else:
            r[p] = 0
            X = None

    pred = model.predict(X) #['Healthy control', 'Myocardial infarction', 'Bundle branch block', 'Cardiomyopathy']

    return X

while True:
    preds = make_preds(mqttc.storage.data)
    print(f'Preds : {preds}')
    time.sleep(4)
    