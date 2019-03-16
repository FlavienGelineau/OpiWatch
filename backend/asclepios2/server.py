import paho.mqtt.client as mqtt
import json

from lib.mqtt import on_connect, on_message

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())["development"]
    print(" * Config:", config)

client.connect(config['broker_uri'], port=1883, keepalive=60, bind_address="")
client.loop_forever()