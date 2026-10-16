import os
import ssl
import json
import paho.mqtt.client as mqtt


BROKER = "s410a220.ala.us-east-1.emqxsl.com"
PORT = 8883

USERNAME = os.environ["MQTT_USERNAME"]
PASSWORD = os.environ["MQTT_PASSWORD"]

TOPIC = "smartmat/test/request"

message = {
	"device": "raspberry_pi",
	"message": "Hello from pi!",
	"weight": "4.25",
	"unit": "kg"
}

def on_connect(client, userdata, flags, reason_code, properties):
	if not reason_code.is_failure:
		print("Raspberry pi is connected to EMQX!")

		client.publish(
			TOPIC,
			json.dumps(message),
			qos=1
		)
	else:
		print(f"Connection failed: {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
	print("Message acknowledged by EMQX!")
	client.disconnect()

client = mqtt.Client(
	callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
	client_id="raspberry_pi_publisher"
)

client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

client.on_connect = on_connect
client.on_publish = on_publish

print("Connecting to EMQX...")

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
