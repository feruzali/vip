import cv2
import compare_functions
import telegram_messenger
import time

def detect_face(cap):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # To differentiate the last person
    last_person = 'Not recognized'
    last_emotion = 'neutral'
    count_same_person = 0
    # To execute the code continuously
    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        cropped_image = gray

        # Draw the rectangle around each face and crop the image
        for (x, y, w, h) in faces:
            cropped_image = gray[y:y + h + 30, x:x + w + 30]

        # Save the image
        if len(faces) >= 1:
            status = cv2.imwrite('images/test.jpeg', cropped_image)
            print("image saved " + str(len(faces)))
            person_name = compare_functions.compare_images('images/test.jpeg')
            if last_person == person_name and person_name != 'Unknown':
                # Used to count the same person
                count_same_person += 1
            else:
                count_same_person = 0
            print(count_same_person)
            if last_person != person_name:
                # If the face changes, it will send it to company via Telegram
                if count_same_person <= 3:
                    time.sleep(1)
                    telegram_messenger.send_attendance(person_name)
                    telegram_messenger.send_image('images/test.jpeg')
                # To save the person's last known face
                last_person = person_name
            time.sleep(1)
        else:
            print('no face recognized')

    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows
