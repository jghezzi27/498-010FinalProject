# iLokd - The Facial Recognition Door Lock

This repo contains code for an ESP32 CAM board as well as a server to which the board will send images. See relevant code section information below.

---

## ESP32 Code (ESPClient/*)

Use Arduino IDE and install relevant libraries. Fill in Wifi information and server address. Should work for any ESP32 Cam board, but you may need to change the pin assignments. The main file is ESPClient/CamClient.ino, and the different states of the state machine are managed in their relevant .ino file.

## Server/ML Code (*.py)

Use install script to install. Required libraries listed in requirements.txt. Run server.py, which relies on utils.py, and either decider.py or decider2.py. client.py can be used to test the server.
