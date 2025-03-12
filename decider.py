# Decides on provided images whether they contain faces that match "verified" faces
import os
import shutil
import numpy as np
import face_recognition
from enum import Enum

class Result(Enum):
    SUCCESS = 0,
    FAILURE = 1,
    NOFACE = 2,
    ERROR = -1

# Function to move a file to a subdirectory
def move_to(file_path, subfolder):
    path_name = os.path.dirname(file_path)
    path_name = os.path.join(path_name, subfolder)
    os.makedirs(path_name, exist_ok=True)
    moved_file = os.path.join(path_name, os.path.basename(file_path))
    shutil.move(file_path, moved_file)


# Load in valid faces
class Decider:
    valid_encodings: dict

    def __init__(self):
        self.valid_encodings = {}
        # Initialize Decider
        dataIn = {
            "lock1": {
                "Joe": ["photos/new0.jpg"],
                "Helen": ["photos/new3.jpg"]
            },
        }

        for lock_id in dataIn:
            users = dataIn[lock_id]
            userMap = {}
            for user in users:
                user_images = users[user]
                user_encodings = []

                # Extract face encodings for this lock:user
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
                self.valid_encodings[lock_id] = userMap

        if len(self.valid_encodings) == 0:
            print(f"ERROR: No Valid Faces For Any Locks")
            exit(1)


    # Assess if the image at file_path contains a valid face for lock lock_id
    def Decide(self, lock_id, file_path):
        if lock_id not in self.valid_encodings:
            move_to(file_path, "error")
            return Result.ERROR

        # Verify Photo
        test_image = face_recognition.load_image_file(file_path)
        test_encodings = face_recognition.face_encodings(test_image)

        if len(test_encodings) == 0:
            move_to(file_path, os.path.join(lock_id, "faceless"))
            return Result.NOFACE

        users = self.valid_encodings[lock_id]
        for user in users:
            user_encodings = self.valid_encodings[lock_id][user]
            for i in range(len(test_encodings)):
                results = face_recognition.compare_faces(user_encodings, test_encodings[i])
                for res in results:
                    if res == np.True_:
                        move_to(file_path, os.path.join(lock_id, "success", user))
                        return Result.SUCCESS
        else:
            move_to(file_path, os.path.join(lock_id, "failure"))
            return Result.FAILURE