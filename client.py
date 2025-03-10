import requests
import os

# Replace with your server's endpoint URL
url = 'http://172.28.117.14:5000/upload'  # Update with your server URL

photo_dir = "photos"

# Path to the image you want to send
files = [entry.name for entry in os.scandir(photo_dir) if entry.is_file()]
for image_name in files:
    # Open the image file in binary mode
    with open(os.path.join(photo_dir, image_name), 'rb') as img_file:
        # Prepare the files dictionary for the POST request
        files = {'image': (image_name, img_file, 'image/jpeg')}
        
        # Send the POST request with the image file
        response = requests.post(url, files=files)

        # Print the server's response
        if response.status_code == 200:
            print(response.text)
        else:
            print(f'Error: {response.status_code}')
            print(response.text)
    print()
