import paho.mqtt.client as mqtt
import time
import threading
import os
from dotenv import load_dotenv
import json
# Carica variabili da .env
load_dotenv()

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

PERIODIC_PAYLOAD = "dati_periodici"
PERIODIC_INTERVAL = 60

gateway_payload = json.dumps({
    "id": 1,
    "cus": [1,2,3,4,5,6,7,8,9,10, 50,51,52,53]  # i set in Python non sono serializzabili direttamente
})



DOWNLINK_TOPICS = ["downlink/gateway", "downlink/cu", "downlink/mu"]
UPLINK_TOPICS = ["uplink/gateway", "uplink/cu", "uplink/mu"]

def periodic_cu_payload(cuid):
    return json.dumps(
       {
        "commandId": 1,
        "gateway": 1,
        "cu": cuid,
        "mu": 0,
        "type": "CONFIGURE",
        "cuSettingDTO": {
            "param1": "value1",
            "param2": 10
        },
        "muSettingDTO": {
            "threshold": 42,
            "enabled": True
        }
    }
    )

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
        for topic in ["uplink/gateway"]:#UPLINK_TOPICS:
            client.publish(topic, gateway_payload)
            print(f"[Periodico] Inviato a {topic}: {gateway_payload}")
        time.sleep(PERIODIC_INTERVAL)

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

threading.Thread(target=send_periodic_data, args=(client,), daemon=True).start()

client.loop_forever()
