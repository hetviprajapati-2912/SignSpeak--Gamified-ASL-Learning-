import cv2
import numpy as np
import tensorflow as tf
from gtts import gTTS
import os
import json
import time

# Load label map
with open("../label_map.json", "r") as f:
    label_names = json.load(f)

# Load trained model
model = tf.keras.models.load_model("../model/signspeak_model.h5")

IMG_SIZE = 64

def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))
    normalized = resized.astype("float32") / 255.0
    return normalized.reshape(1, IMG_SIZE, IMG_SIZE, 1)

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")  # Use 'start' on Windows; use 'afplay' for Mac, 'xdg-open' for Linux

# Open webcam
cap = cv2.VideoCapture(0)
predicted_label = ""
last_prediction_time = 0

print("🎥 Starting webcam. Press 's' to speak prediction. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[100:300, 100:300]  # Region of interest
    input_data = preprocess_frame(roi)
    predictions = model.predict(input_data)
    label_index = np.argmax(predictions)
    confidence = predictions[0][label_index]

    predicted_label = label_names[label_index]

    # Draw box and prediction
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)
    cv2.putText(frame, f"{predicted_label} ({confidence*100:.1f}%)", (100, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    cv2.imshow("SignSpeak - Gesture Detection", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and time.time() - last_prediction_time > 2:
        speak(predicted_label)
        last_prediction_time = time.time()

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
