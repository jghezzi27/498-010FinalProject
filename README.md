# 🔐 iLokd - The Facial Recognition Door Lock

This repository powers the backend for our ESP32-CAM-based Smart Door Lock system. The server receives image frames from the embedded device, runs a machine learning model to validate access, and responds with authentication results.

This repo contains code for an ESP32 CAM board as well as a server to which the board will send images. See relevant code section information below.

---

## ESP32 Code (ESPClient/*)

Use Arduino IDE and install relevant libraries. Fill in Wifi information and server address. Should work for any ESP32 Cam board, but you may need to change the pin assignments. The main file is ESPClient/CamClient.ino, and the different states of the state machine are managed in their relevant .ino file.

## Server/ML Code (*.py)

Use install script to install. Required libraries listed in requirements.txt. Run server.py, which relies on utils.py, and either decider.py or decider2.py. client.py can be used to test the server.


---

## 📍 Hosted Server Info

Our backend server is hosted on AWS EC2:

**Public DNS:**

Access the public DNS from the EC2 instance dashboard that you instantiated 

---

## 📦 API Endpoint

### `POST /upload`

Uploads a single frame from the ESP32-CAM.

- **URL**:  
  `http://[your_public_DNS].us-east-2.compute.amazonaws.com/upload`

- **Method**: `POST`

- **Payload**:  
  Send the image as multipart/form-data or base64 (depending on ESP32 setup).

- **Response**:
  ```json
  {
    "status": "SUCCESS" | "FAIL" | "NOFACE" | "ERROR"
  }

##🧠 Server Functionality
- Accepts an image frame from the embedded system
- Runs our ML model to detect and identify a face
- Returns an access decision back to the ESP32
- Can optionally trigger a log or a smart lock actuator