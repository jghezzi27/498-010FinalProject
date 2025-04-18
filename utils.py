from enum import Enum

class Result(Enum):
    SUCCESS = 0,
    FAIL = 1,
    NOFACE = 2,
    ERROR = -1

# Function to move a file to a subdirectory
def move_to(file_path, subfolder):
    path_name = os.path.dirname(file_path)
    path_name = os.path.join(path_name, subfolder)
    os.makedirs(path_name, exist_ok=True)
    moved_file = os.path.join(path_name, os.path.basename(file_path))
    shutil.move(file_path, moved_file)
