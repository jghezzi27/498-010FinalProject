from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import face_recognition
import numpy as np

# Load in valid faces
valid_photo = "photos/new0.jpg"
valid_image = face_recognition.load_image_file(valid_photo)
valid_encodings = face_recognition.face_encodings(valid_image)
if len(valid_encodings) == 0:
    print("ERROR: No Valid Face")
    exit(1)

# Initialize the Flask app
app = Flask(__name__)

# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint to handle image upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the 'image' part exists in the form
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in request'}), 400

    file = request.files['image']

    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # If the file is valid
    if file and allowed_file(file.filename):
        # Secure the filename to prevent directory traversal
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file to the upload folder
        file.save(file_path)

        # Verify Photo
        test_image = face_recognition.load_image_file(file_path)
        test_encodings = face_recognition.face_encodings(test_image)

        if len(test_encodings) == 0:
            return jsonify({'message': f'No Faces found within image! Saved as {filename}'}), 200

        permission = False
        for i in range(len(test_encodings)):
            results = face_recognition.compare_faces(valid_encodings, test_encodings[i])
            for res in results:
                if res == np.True_:
                    permission = True
            print(f"{valid_photo}, {file_path}-{i}: {results}")
        
        if permission:
            return jsonify({'message': f'Permission Granted! Saved as {filename}'}), 200
        else:
            return jsonify({'message': f'Permission NOT Granted! Saved as {filename}'}), 200
    else:
        return jsonify({'error': 'Invalid file format. Only jpg, jpeg, and png are allowed.'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all available IPs on port 5000
