from flask import Flask, request, jsonify
import os
import shutil
from werkzeug.utils import secure_filename
import face_recognition
import numpy as np
import datetime


# Load in valid faces
dataIn = {
    "lock1": {
        "Joe": ["photos/new0.jpg"],
        "Helen": ["photos/new3.jpg"]
    },
}

valid_encodings = {}
for lock_id in dataIn:
    users = dataIn[lock_id]
    userMap = {}
    for user in users:
        user_images = users[user]
        user_encodings = []

        for photo in user_images:
            image = face_recognition.load_image_file(photo)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) == 0:
                continue
            for enc in encodings:
                user_encodings.append(enc)

        if len(user_encodings) != 0:
            userMap[user] = user_encodings
    if len(userMap) == 0:
        print(f"ERROR: No Valid Faces For Lock {lock_id}")
    else:
        valid_encodings[lock_id] = userMap

if len(valid_encodings) == 0:
    print(f"ERROR: No Valid Faces For Any Locks")
    exit(1)


# Initialize the Flask app
app = Flask(__name__)

# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to move a file to a subdirectory
def move_to(file_path, subfolder):
    path_name = os.path.dirname(file_path)
    path_name = os.path.join(path_name, subfolder)
    os.makedirs(path_name, exist_ok=True)
    moved_file = os.path.join(path_name, os.path.basename(file_path))
    shutil.move(file_path, moved_file)


# Endpoint to handle image upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the 'image' part exists in the form
    if 'image' not in request.files:
        return jsonify({'Error': 'No image part in request'}), 400

    file = request.files['image']

    # If no file is selected
    if file.filename == '':
        return jsonify({'Error': 'No selected file'}), 400

    if 'lock_id' not in request.form:
        return jsonify({'Error': 'No lock_id in request'}), 400

    lock_id = request.form["lock_id"]
    if lock_id not in valid_encodings:
        return jsonify({'Error': f"No lock with id {lock_id}"}), 400

    # If the file is valid
    if file and allowed_file(file.filename):
        # Add timestamp to filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name, file_extension = os.path.splitext(file.filename)
        new_filename = f"{file_name}_{timestamp}{file_extension}"

        # Secure the filename to prevent directory traversal
        filename = secure_filename(new_filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        
        # Save the file to the upload folder
        file.save(file_path)

        # Verify Photo
        test_image = face_recognition.load_image_file(file_path)
        test_encodings = face_recognition.face_encodings(test_image)

        if len(test_encodings) == 0:
            move_to(file_path, "faceless")
            return jsonify({'message': f'No Faces found within image!'}), 200

        users = valid_encodings[lock_id]
        for user in users:
            user_encodings = valid_encodings[lock_id][user]
            for i in range(len(test_encodings)):
                results = face_recognition.compare_faces(user_encodings, test_encodings[i])
                for res in results:
                    if res == np.True_:
                        move_to(file_path, "success")
                        return jsonify({'message': f'Permission Granted {lock_id}:{user}!'}), 200
        else:
            move_to(file_path, "failure")
            return jsonify({'message': f'Permission NOT Granted to {lock_id}!'}), 200
    else:
        return jsonify({'error': 'Invalid file format. Only jpg, jpeg, and png are allowed.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all available IPs on port 5000
