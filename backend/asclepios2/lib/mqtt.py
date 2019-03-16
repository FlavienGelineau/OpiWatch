def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("qkcrE0UDj4")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))