import paho.mqtt.client as mqtt
import json

def update(d, p, v, memory_size=1024):
    d[p].append(v)
    if len(d[p]) == (memory_size + 1):
        d[p].pop(0)

class Storage:
    def __init__(self):
        self.watched_patients = set()
        self.data = dict()
        self.counts = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")
    
def on_message(client, userdata, msg):
    patient = msg.topic
    value = json.loads(msg.payload.decode("utf-8","ignore"))
    if patient not in client.storage.watched_patients:
        client.storage.data[patient] = []
        client.storage.counts[patient] = 0
        client.storage.watched_patients.add(patient)
    client.storage.counts[patient] += 1
    update(client.storage.data, patient, value)
    if client.storage.counts[patient] % 1024 == 0:
        print(f'Patient {patient} has lived a full cycle')

class Client(mqtt.Client):
    
    def __init__(self):
        super().__init__()
        self.storage = Storage()
        self.on_connect = on_connect
        self.on_message = on_message
