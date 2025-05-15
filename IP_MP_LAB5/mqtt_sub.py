import paho.mqtt.client as mqtt
from imdb import imdb_search
from imdb import imdb_searchbox

MQTT_Topic = "Movies/content"
#mqttBroker = "192.168.132.34"
mqttBroker = "192.168.64.34"

def on_message(client, userdata, message):
    print("received message: ", str(message.payload.decode("utf-8")))
    if len(message.payload.decode("utf-8")) > 0:
        content = imdb_search(str(message.payload.decode("utf-8")), keep_open=True)
        #content = imdb_searchbox("http://www.imdb.com", str(message.payload.decode("utf-8")))
        client.publish("expo/test", str(content))

# Create client with callback API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Sniffer")  # <-- Key change here
#content = imdb_search(str(message.payload.decode("utf-8")), keep_open=True)
client.connect(mqttBroker)
client.subscribe(MQTT_Topic)
client.on_message = on_message
client.loop_forever()