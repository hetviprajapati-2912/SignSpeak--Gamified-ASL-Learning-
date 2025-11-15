import cv2
import numpy as np
from keras.models import load_model
import pyttsx3
import time
import os

# Load the trained model from the correct path
model_path = "webapp/model/signspeak_model.h5"

if not os.path.exists(model_path):
    print(f"ERROR: Model file not found at path: {model_path}")
    exit()

model = load_model(model_path)

# List of classes (A to Z)
class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
               'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
               'Y', 'Z', 'del', 'nothing', 'space']

print("Classes found:", class_names)


# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 130)

def speak(prediction):
    """Speak out the prediction"""
    engine.say(prediction)
    engine.runAndWait()

# Try to connect to webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: No webcam found. Trying alternative camera index (1)...")
    cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("ERROR: No working webcam found. Please check your camera connection or drivers.")
    exit()

print("SUCCESS: Webcam connected. Starting real-time prediction...")

prev_prediction = ""
last_spoken_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("WARNING: Unable to read frame from camera.")
        break

    # Flip and define region of interest
    frame = cv2.flip(frame, 1)
    roi = frame[100:400, 100:400]

    # Preprocess ROI for model
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    roi_resized = cv2.resize(roi_gray, (64, 64))
    roi_normalized = roi_resized / 255.0
    roi_reshaped = np.reshape(roi_normalized, (64, 64, 1))
    roi_input = np.expand_dims(roi_reshaped, axis=0)

    # Predict from model
    predictions = model.predict(roi_input)
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    # Display box and prediction
    cv2.rectangle(frame, (100, 100), (400, 400), (255, 0, 0), 2)
    cv2.putText(
        frame,
        f"{predicted_class} ({confidence:.2f})",
        (100, 450),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    # Speak prediction
    if confidence > 0.85 and predicted_class != prev_prediction:
        current_time = time.time()
        if current_time - last_spoken_time > 2:
            speak(predicted_class)
            prev_prediction = predicted_class
            last_spoken_time = current_time

    # Show the video frame
    cv2.imshow("SignSpeak - Real-Time Sign Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Program terminated by user.")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
