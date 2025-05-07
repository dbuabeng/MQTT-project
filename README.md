## MQTT Privacy-Enhanced Messaging System

## Project Description
In this project I simulated MQTT communication between victims, drones (broker) and the C2 system during a calamity. Privacy threats are analyzed using the LINDDUN framework and two privacy-enhancing technologies (PETs) are implemented: Tokenization and Encryption.

## Tools and Technologies I Used
	- Python 3.12.2
	- paho-mqtt library
	- cryptography library (Fernet encryption)
	- Mosquitto MQTT Broker (2.0.21a for Windows)
	- Windows 11 64-bit OS

## Installation Instructions

1. Install Python Libraries
	pip install paho-mqtt
	pip install cryptography
2. Install Mosquitto Broker
Downloaded from https://mosquitto.org/download/

3. Mosquitto Broker Setup:
	- Installed Mosquitto Broker version 2.0.21a for Windows.
	- Default configuration used (port 1883 without authentication or TLS).
	- After that I verifed broker is running in services.msc.
	- Privacy protection is applied at the application layer (tokenization and encryption of payloads).


## How to Run the Project
1. First I started Subscriber:
	python subscriber.py
2. Second I started Publisher in a new Command Prompt:
	python publisher.py

The subscriber will receive and decrypt messages sent by the publisher.

I manually generated the encryption key. It is stored inside docs/encryptionKey.key.

In these programs messages are encrypted and tokenized for privacy protection.

## Link to YouTube Video
https://youtu.be/nSvhTHZ3BNM
