# We used the face-recognition library to recognize the faces
#https://github.com/ageitgey/face_recognition
import face_recognition

cutoff = 0.5

# Load some images to compare against
azamjon_image = face_recognition.load_image_file("images/javo.jpeg")

# Get the face encodings for the known images
javo_encoding = face_recognition.face_encodings(javo_image)[0]

known_encodings = [
    (javo_encoding, "Javokhir"),
]

# To compare the faces of the known people and return the name of person respectively
def compare_images(img_src):
    img1 = face_recognition.load_image_file(img_src)
    if len(face_recognition.face_encodings(img1)) == 0:
        return 'Unknown'
    img1_face_encoding = face_recognition.face_encodings(img1)[0]
    face_distances = face_recognition.face_distance(list(map(lambda n: n[0], known_encodings)), img1_face_encoding)
    return get_face_name(face_distances)

# To get the name of the known people
def get_face_name(face_distances):
    index_min = min(range(len(face_distances)), key=face_distances.__getitem__)
    min_dist = min(face_distances)
    if min_dist > cutoff:
        return 'Unknown'
    else:
        return known_encodings[index_min][1]