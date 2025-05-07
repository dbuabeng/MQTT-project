## Disaster Messaging System with Privacy Enhancements

## Scenario Description

In this project we simulate a disaster scenario where real-time communication is critical to coordinate rescue efforts. Victims trapped in affected areas need to send their locations and help requests securely. Drones, acting as mobile brokers, collect messages from victims and forward them to a central Command and Control (C2) system.

We built this system using the MQTT protocol:
	- Victims act as publishers, sending help messages.
	- Drones serve as brokers (using Mosquitto MQTT broker).
	- The C2 system subscribes to messages and coordinates the rescue.

While the system enables timely communication, it also creates privacy risks. Attackers could intercept sensitive information like victim identities or locations.  
Our goal was to build the system and strengthen its privacy by applying threat modeling and privacy-enhancing technologies.

## Threat Model (LINDDUN Framework)

Using the LINDDUN framework, we identified the following potential privacy threats:

| Threat                      | Risk                                                              |
|:----------------------------|:------------------------------------------------------------------|
| Linkability                 | Attackers could link multiple messages to the same victim.        |
| Identifiability             | Victim identities (names, device IDs) could be revealed.          |
| Non-repudiation             | Victims could not deny sending certain messages later.            |
| Detectabilit                | Attackers could detect when and how often victims communicate.    |
| Disclosure of Information   | Sensitive location or help requests could be exposed.             |
| Unawareness                 | Victims may not realize how much data is being shared.            |
| Non-compliance              | The system may violate privacy laws like GDPR without protections.|

![image](https://github.com/user-attachments/assets/075faaab-feb1-47b4-aac0-24d55b391777)

## Vulnerability Analysis by Component and Data Flow

| Label | Element               | Description                                   | Potential Vulnerability                               | LINDDUN Category                         | Mitigation                                      |
|-------|------------------------|-----------------------------------------------|--------------------------------------------------------|------------------------------------------|--------------------------------------------------|
| E1    | Victim                 | Provides sensitive info like location, health, distress status | Unauthorized collection or use of PII                  | Identifiability, Unawareness             | Consent management, data minimization, privacy notices |
| P1    | User App               | Publishes MQTT messages with victim data      | Hardcoded credentials, lack of encryption              | Linkability, Detectability              | App-level TLS, dynamic client IDs               |
| DF1   | Victim to App          | Sends victim data to app                      | Unencrypted transmission                               | Identifiability                          | Encrypt at source or secure channel (HTTPS)     |
| DF2/DF3/DF4 | Drone broker network | Relays messages to edge/cloud              | Broker spoofing, bridge message leakage                | Linkability, Non-compliance              | Use TLS/SSL, authenticate brokers               |
| P2/P3 | Broker Forwarders      | Route messages to cloud                       | MQTT topic leakage, no ACLs                            | Linkability, Detectability               | Enforce topic-level ACLs, broker auth           |
| DF5/DF6 | Message to Gateway   | MQTT over TCP                                 | Lack of message integrity or replay protection         | Detectability                            | Use HMAC, timestamps, TLS                       |
| P4    | Cloud Gateway          | Entry point to cloud layer                    | Cloud misconfigurations, weak auth                     | Non-compliance, Identifiability          | OAuth2, federated identity, rate limiting       |
| DF7   | MQTT Payload           | Message forwarded to data layer               | Payload in plaintext, possible data inference          | Identifiability                          | Encrypt payload (AES over MQTT)                 |
| DF8   | Authentication         | Auth before DB insert                         | Weak credentials, brute-force login                    | Non-repudiation                          | Multi-factor auth, rate limiting                |
| P5    | Message Parser         | Processes incoming payload                    | Poor input validation, injection risk                  | Non-compliance                           | Validate/sanitize data before DB insertion      |
| DF9   | SQL INSERT             | Writes to MySQL DB                            | SQL Injection, logging sensitive info                  | Non-repudiation                          | Prepared statements, encryption-at-rest         |
| DS1   | MySQL Database         | Stores mission-critical data                  | Data breach, poor access control                       | Non-compliance, Identifiability          | Column-level encryption, access logs            |
| DF10/DF11 | Query to DB and results | Dashboard queries                        | Inference via pattern queries                          | Linkability, Detectability              | Limit user roles, anonymized query results      |
| P6    | C2 Dashboard           | Queries and visualizes                        | Overexposure to operators, session hijack              | Unawareness, Non-compliance              | RBAC, secure sessions                           |
| DF12  | Visualization to CMC   | Visual output to operator                     | Shoulder-surfing, unauthorized viewing                 | Detectability, Identifiability           | Redact sensitive fields, audit logs             |
| E2    | CMC Operator           | Interacts with dashboard                      | Misuse of data, privacy violations                     | Unawareness, Non-compliance              | Training, privacy policies                      |



## MQTT-Specific Privacy Threats

In an MQTT-based messaging system additional privacy risks exist:

	- Linkability Threat: Attackers could subscribe to wildcard topics and monitor message flows, linking multiple messages back to the same victim based on timing, patterns or payload structures.
  
	- Disclosure of Information: If MQTT topics are not secured with access control and encryption, attackers could eavesdrop on open topics and capture sensitive victim information like their location or help request contents.

	- Detectability: Even if the message content is encrypted an attacker could still detect when victims are active by observing when messages are published, potentially inferring patterns about victim movement or behavior.

These risks show why strong application-layer protections like tokenization and encryption are crucial even when using lightweight protocols like MQTT.

## Privacy Enhancements Implemented

To address these risks, we integrated two privacy-enhancing technologies (PETs):

### 1. Tokenization
We replaced real victim identifiers (For example "Victim1") with random UUID tokens.  
This prevents direct identification if messages are intercepted.


### 2. Encryption
We encrypted all MQTT message payloads using symmetric encryption (Fernet).  
This ensures that even if messages are intercepted, the data remains unreadable without the correct decryption key.

Together, these methods greatly strengthen privacy protection in the system.

## Before and After Applying Privacy Enhancements

| Aspect                | Before PETs                 | After PETs                                |
|:----------------------|:----------------------------|:------------------------------------------|
| Victim Identifier     | Clear names like "Victim1"  | Random token like "4ff9d258-..."          |
| Message Content       | Plain text, easily readable | Fully encrypted & unreadable without key  |
| Attack Risk           | High chance of data leak    | Very low risk                             |
| Regulatory Compliance | Not privacy-compliant       | Strongly aligned with privacy principles  |

## Evaluation of Privacy Controls

We evaluated the impact of the privacy controls based on several factors:

	- Message Confidentiality: Encryption protects sensitive location and identity data.
	- Victim Anonymity: Tokenization prevents direct linking of victims to messages.
	- System Overhead: There was a slight increase in message size due to encryption, but no noticeable impact on  performance.
	- Trade-offs: The system became slightly more complex, but the privacy improvements outweighed the added complexity.

Overall, the protections significantly improved the system’s privacy posture without affecting usability.

## Final Reflections

Through this project, we demonstrated how privacy can be integrated into real-time communication systems in disaster scenarios.  
By applying a structured threat model (LINDDUN) and implementing simple but effective PETs we were able to design a system that protects the identities and locations of victims without sacrificing performance.

Privacy must be a priority even during emergencies and with thoughtful design, it is possible to achieve both security and usability.
