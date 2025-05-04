# import required libraries

import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet

# Defining broker address and topic
brokerAddr = "localhost"
topic = "disaster/location"

# Load the symmetric encryption key used by publisher
with open("../docs/encryptionKey.key", "rb") as keyFile:
    encryKey = keyFile.read()
cipherSuite = Fernet(encryKey)

# Define function for callback when a message is received
def onMessage(clientMqtt, userData, msgInfo):
    encryptedPayload = msgInfo.payload
    try:
        decryptedPayload = cipherSuite.decrypt(encryptedPayload).decode()
        print(f"Received decrypted message: {decryptedPayload}")
    except Exception as error:
        print(f"Error decrypting message: {error}")

# Create a new MQTT client instance
clientMqtt = mqtt.Client(client_id="c2Subscriber", protocol=mqtt.MQTTv311)
clientMqtt.on_message = onMessage

# Connect to broker
clientMqtt.connect(brokerAddr)

# Subscribe to topic
clientMqtt.subscribe(topic)

# Continuously listen for incoming encrypted messages
print("Connected to broker. Waiting for encrypted messages...")
clientMqtt.loop_forever()
