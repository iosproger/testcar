import json
import random
import time
import requests
import paho.mqtt.client as mqtt

# Define the MQTT settings
MQTT_BROKER = "mqtt.iotserver.uz"
MQTT_PORT = 1883
MQTT_USER = "userTTPU"
MQTT_PASSWORD = "mqttpass"
MQTT_TOPIC = "ttpu/car/gps"  # Use wildcard to subscribe to all topics under ttpu/

# Define the callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")
    try:
        payload = msg.payload.decode().replace("'", '"')
        d = json.loads(payload)
        msg_to_send_to_server(d)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")

def msg_to_send_to_server(data):
    u = "192.168.0.102:8001"
    node_name = data.get("id")
    latitude = data.get("Latitude")
    longitude = data.get("Longitude")

    if node_name and latitude and longitude:
        url = f"http://{u}/loc/n/{node_name}"
        payload = {
            'latitude': f'{latitude}',
            'longitude': f'{longitude}'
        }
        headers = {}

        try:
            response = requests.put(url, headers=headers, data=payload)
            print(response.text)
        except requests.RequestException as e:
            print(f"Failed to send request: {e}")
    else:
        print("Invalid data received")

# Create an MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop
client.loop_start()

# Keep the script running to receive messages
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Disconnecting from broker...")
    client.disconnect()
    client.loop_stop()
