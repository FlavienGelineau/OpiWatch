from lib.mqtt import Client
import random
import json
import time

mqttc = Client()
with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())["development"]
    print(" * Config:", config)
mqttc.connect(config['broker_uri'], port=1883, keepalive=60)
mqttc.loop_start()

def make_preds(d):
    r = {}
    for p in d.keys():
        if len(d[p]) == 1024:
            print(d[p][0])
            r[p] = d[p][0]["time"]

        else:
            r[p] = 0
    return r

while True:
    preds = make_preds(mqttc.storage.data)
    print(f'Preds : {preds}')
    time.sleep(4)
    