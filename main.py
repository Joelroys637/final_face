import face_recognition
import cv2
import numpy as np
import os
import streamlit as st
import sqlite3
from datetime import date
from PIL import Image

# Initialize Streamlit app
st.title("Face Recognition Attendance System")
st.write("Detect faces and mark attendance using an image captured from your webcam.")
lecture_name = st.text_input('Enter subject lecture name:')
# Set up database
try:


    conn = sqlite3.connect('attendance_db.db')
    c = conn.cursor()
    safe_table_name = ''.join(e for e in lecture_name if e.isalnum())
    query=f"CREATE TABLE IF NOT EXISTS {safe_table_name} (name TEXT, date TEXT)"
    c.execute(query)
    conn.commit()
except:
    pass





# Load known faces from the 'images' folder
CurrentFolder = os.getcwd()
images_folder = os.path.join(CurrentFolder, 'images')
known_face_encodings = []
known_face_names = []

# Load known images and encode faces
for filename in os.listdir(images_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(images_folder, filename)
        name = os.path.splitext(filename)[0]  # Name from filename
        image = face_recognition.load_image_file(image_path)
        try:
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
        except IndexError:
            st.warning(f"No face found in {filename}. Skipping.")

# Lecture input


if not lecture_name:
    st.stop()

# Capture image with Streamlit
captured_image = st.camera_input("Capture an image")

if captured_image is not None:
    # Convert the image to OpenCV format
    image = Image.open(captured_image)
    frame = np.array(image)

    # Resize for faster face detection
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]  # Convert BGR to RGB

    # Face recognition on the captured frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Find the closest match
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        # Check attendance in database
        face_names.append(name)
        if name != "Unknown":
            c.execute(f"SELECT * FROM {safe_table_name} WHERE name = ? AND date = ?", (name, str(date.today())))
            result = c.fetchone()
            if not result:
                c.execute(f"INSERT INTO {safe_table_name} (name, date) VALUES (?, ?)", (name, str(date.today())))
                st.write(f"Attendance marked for {name}")
                conn.commit()
            else:
                st.write(f"Attendance already marked for {name}")

    # Annotate and display image
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display processed frame
    st.image(frame, channels="BGR")

# Close database connection
conn.close()
