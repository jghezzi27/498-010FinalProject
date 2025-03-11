# Hosts a server that receives images and sends responses
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import datetime
from decider import Decider, Result

# Initialize the Flask app
app = Flask(__name__)

# Initialize Decider
dataIn = {
    "lock1": {
        "Joe": ["photos/new0.jpg"],
        "Helen": ["photos/new3.jpg"]
    },
}

decider = Decider(dataIn)

# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "iLokd Server"

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

    if 'lock_id' not in request.form:
        return jsonify({'error': 'No lock_id in request'}), 400

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

        # Get permission for file
        lock_id = request.form["lock_id"]
        status, message = decider.Decide(lock_id, file_path)
        if status == Result.ERROR:
            return jsonify({'error': message}), 400
        return jsonify({'message': message}), 200          

    else:
        return jsonify({'error': 'Invalid file format. Only jpg, jpeg, and png are allowed.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all available IPs on port 5000
