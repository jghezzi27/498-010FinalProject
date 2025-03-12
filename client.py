# Simulates a client (a real client will be the ESP32 CAM Module)

import requests
import os
import time

# Replace with your server's endpoint URL
url = 'http://127.0.0.1:5000/upload'  # Update with your server URL

photo_dir = "photos"

# Path to the image you want to send
files = [entry.name for entry in os.scandir(photo_dir) if entry.is_file()]
for image_name in files:
    # Open the image file in binary mode
    with open(os.path.join(photo_dir, image_name), 'rb') as img_file:
        # Prepare the files dictionary for the POST request
        files = {'image': (image_name, img_file, 'image/jpeg')}
        data = {"lock_id": "lock1"}

        # Send the POST request with the image file
        sendTime = time.time()
        response = requests.post(url, files=files, data=data)
        returnTime = time.time()
        duration = returnTime - sendTime

        # Print the server's response
        if response.status_code == 200:
            print(f"{image_name}:\n\tResult: {response.json()['message']}\n\tLatency: {duration} s")
        else:
            print(f'Error: {response.status_code}')
            print(f"{image_name}:\n\tResult: {response.json()['error']}\n\tLatency: {duration} s")
