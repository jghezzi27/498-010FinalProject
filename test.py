import face_recognition
import numpy as np

# Example usage
embeddings = []
for i in range(5):
    img_path = 'photos/test' + str(i) + '.jpg'
    print(f"Testing {img_path}")
    known_image = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(known_image)
    print(len(encoding))
    for j, emb in enumerate(encoding):
        embeddings.append((img_path + "-" + str(j), emb))

for i in range(len(embeddings)):
    for j in range(i+1, len(embeddings)):
        results = face_recognition.compare_faces([embeddings[i][1]], embeddings[j][1])
        print(f"{embeddings[i][0]}, {embeddings[j][0]}: {results == np.True_}")
