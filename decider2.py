# Decides on provided images whether they contain faces that match "verified" faces
import os
import shutil
import numpy as np
from utils import Result, move_to
from deepface import DeepFace

# Load in valid faces
class Decider:
    valid_encodings: dict

    def __init__(self):
        # Define paths
        self.database_paths = {"lock1":"photodb/"} # Folder containing images

    def Decide(self, lock_id, file_path):
        if lock_id not in self.database_paths:
            move_to(file_path, "error")
            return Result.ERROR

        # Verify Photo
        results = DeepFace.find(img_path=file_path, db_path=self.database_paths[lock_id], 
                                model_name="ArcFace", detector_backend="retinaface", 
                                distance_metric="cosine", enforce_detection=True)

        # Print the results
        min_distance = results[0]['distance'].min()

        if results and results[0]['distance'].min() < 0.35:  # Adjust threshold as needed
            return Result.SUCCESS
        else:
            return Result.FAIL


if __name__ == '__main__':
    photo_dir = "photos"
    # Path to the image you want to send
    files = [entry.name for entry in os.scandir(photo_dir) if entry.is_file()]
    with open("out.txt", "w") as fout:
        for image_name in files:
            input_image = os.path.join(photo_dir, image_name)
            decider = Decider()
            fout.write(f"{input_image}: {decider.decide('lock1', input_image).name}\n")
            print(f"{input_image}: {decider.decide('lock1', input_image).name}")

