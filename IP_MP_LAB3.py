from http import client 
import paho.mqtt.client as mqtt 
import time

def connect_broker(broker_address, client_name):
    #client = mqtt.Client(client_name)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_name)
    client.connect(broker_address)
    time.sleep(1)
    client.loop_start()

    return client

if __name__ == "__main__":
    server = "broker.hivemq.com"
    client_name = "mqttx_45a03b655"
    client = connect_broker(server,client_name)
    try:
        while True:
            message=input("Sent some random message:")
            client.publish("testtopic/temperature",message)
    except KeyboardInterrupt:
            client.disconnect()
            client.loop_stop()