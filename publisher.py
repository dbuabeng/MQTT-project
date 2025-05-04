# import required libraries

import paho.mqtt.client as mqtt
import time
import uuid
from cryptography.fernet import Fernet

# Defining broker address and topic
brokerAddr = "localhost"
topic = "disaster/location"

# Load the existing encryption key that was manually generated
with open("../docs/encryptionKey.key", "rb") as keyFile:
    encryKey = keyFile.read()

# Create encryption tool using the loaded key    
cipherSuite = Fernet(encryKey)

# Create a new MQTT client instance
clientMqtt = mqtt.Client(client_id="victimPublisher", protocol=mqtt.MQTTv311)

# Connect to the broker
clientMqtt.connect(brokerAddr)

# Loop to simulate 5 different victim messages being sent
for msgCounter in range(5):
    victimToken = str(uuid.uuid4())
    locationInfo = f"{msgCounter * 10},{msgCounter * 20}"
    plainMsg = f"Token:{victimToken} Location:{locationInfo}"
    
    # Show size of the unencrypted message
    plainMsgSize = len(plainMsg.encode())
    print(f"Plain Message Size: {plainMsgSize} bytes")
    
    # Encrypt the message
    encryMsg = cipherSuite.encrypt(plainMsg.encode())
    
    # Measure and show encrypted message size
    encryMsgSize = len(encryMsg)
    print(f"Encrypted Message Size: {encryMsgSize} bytes")
    
    # Publish encrypted message
    clientMqtt.publish(topic, encryMsg)
    print(f"Published encrypted message: {plainMsg}")
    print("-" * 60)
    
    # Wait for 3 seconds before sending the next message    
    time.sleep(3)

# Disconnect after sending
clientMqtt.disconnect()
