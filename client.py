import requests

# Replace with your server's endpoint URL
url = 'http://172.28.117.14:5000/upload'  # Update with your server URL

# Path to the image you want to send
image_path = 'photos/test0.jpg'  # Update with your image path

# Open the image file in binary mode
with open(image_path, 'rb') as img_file:
    # Prepare the files dictionary for the POST request
    files = {'image': ('test_image.jpg', img_file, 'image/jpeg')}
    
    # Send the POST request with the image file
    response = requests.post(url, files=files)

    # Print the server's response
    if response.status_code == 200:
        print(response.text)
    else:
        print(f'Error: {response.status_code}')
        print(response.text)
