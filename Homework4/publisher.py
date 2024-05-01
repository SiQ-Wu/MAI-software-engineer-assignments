import numpy as np
import paho.mqtt.client as mqtt
import time

broker = "broker.emqx.io"
port = 1883
topic = "movement_simulation"

g = 9.8

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT server!")
        client.subscribe(topic)
    else:
        print(f"Failed to connect, result code {0}".format(str(rc)))
        
def on_publish(client, userdata, mid):
    print('Sending data')
        
def mqtt_pub(vx0, vy0, sim_t):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(broker, port, 60)
    client.loop_start()
    
    t = np.linspace(0,sim_t,sim_t+1)
    vx = vx0 - g * t
    vy = vy0 + t * 0
    x = vx0 * t -  0.5 * g * t ** 2
    y = vy0 * t
    
    for i in range(len(t)):

        data = str(t[i]) + ' ' + str(x[i]) + ' ' + str(y[i]) + ' ' + str(vx[i]) + ' ' + str(vy[i])
        client.publish(topic=topic, payload=data, retain=False)
        time.sleep(1)
        

if __name__ == '__main__':
    '''
    vx, vy, t = input('Input Vertical speed, Horizontal speed and Simulation time, split by space').split(' ')
    vx = int(vx)
    vy = int(vy)
    t = int(t)
    
    '''
    mqtt_pub(100, 15, 15)
