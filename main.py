import paho.mqtt.client as mqtt
import time
import threading
import os
from dotenv import load_dotenv

# Carica variabili da .env
load_dotenv()

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

PERIODIC_PAYLOAD = "dati_periodici"
PERIODIC_INTERVAL = 30

DOWNLINK_TOPICS = ["downlink/gateway", "downlink/cu", "downlink/mu"]
UPLINK_TOPICS = ["uplink/gateway", "uplink/cu", "uplink/mu"]

def on_connect(client, userdata, flags, rc):
    print("Connesso con codice di risultato:", rc)
    for topic in DOWNLINK_TOPICS:
        client.subscribe(topic)
        print(f"Sottoscritto a: {topic}")

def on_message(client, userdata, msg):
    print(f"Ricevuto messaggio su {msg.topic}: {msg.payload.decode()}")
    uplink_topic = msg.topic.replace("downlink", "uplink")
    client.publish(uplink_topic, msg.payload)
    print(f"Inviato a {uplink_topic}: {msg.payload.decode()}")

def send_periodic_data(client):
    while True:
        for topic in UPLINK_TOPICS:
            client.publish(topic, PERIODIC_PAYLOAD)
            print(f"[Periodico] Inviato a {topic}: {PERIODIC_PAYLOAD}")
        time.sleep(PERIODIC_INTERVAL)

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

threading.Thread(target=send_periodic_data, args=(client,), daemon=True).start()

client.loop_forever()
