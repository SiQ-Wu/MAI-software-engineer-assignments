import numpy as np
import paho.mqtt.client as mqtt
import time

broker = "broker.emqx.io"
port = 1883
topic = "movement_simulation"

t = []
x = []
y = []
vx = []
vy = []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT server!")
        client.subscribe(topic)
    else:
        print(f"Failed to connect, result code {0}".format(str(rc)))
        
def on_message(client, userdata, msg):

    data = msg.payload.decode('utf-8').split(' ')
    t.append(float(data[0]))
    x.append(float(data[1]))
    y.append(float(data[2]))
    vx.append(float(data[3]))
    vy.append(float(data[4]))
    print("t={}\tx={}\ty={}\tvx={}\tvy={}\n".format(data[0],data[1],data[2],data[3],data[4]))
    time.sleep(1)

    
def mqtt_sub():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, 60)
    client.loop_start() 
    
if __name__ == '__main__':
    mqtt_sub()
