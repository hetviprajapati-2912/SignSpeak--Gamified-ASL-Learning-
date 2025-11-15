# SignSpeak 🔤🧠🔊

SignSpeak is a Real-Time American Sign Language (ASL) recognition app powered by deep learning.

## 💡 Features

- Trained CNN model (TensorFlow/Keras)
- Real-time webcam gesture recognition
- Text-to-Speech using Google TTS
- Easy-to-extend structure (add Flashcards, Sentence Prediction, Django)

## 🧪 How to Run

1. Install Dependencies

cd "c:\HETVI-PERSONAL\SIGNSPEAK(Final)\Main\SignSpeak"
pip install -r requirements.txt

2. Run Desktop App (Real-time ASL Detection)

python realtime_predict.py

Controls: Press q to quit

Features: Live webcam detection + voice output

Requirements: Desktop only (won't work on mobile)

3. Run Web Application

cd webapp
python manage.py runserver 

📱 Access on Mobile

Find Your IP Address:
ipconfig
Look for IPv4 address (e.g., 192.168.1.100)

Open on Mobile:
Connect phone to same WiFi

Browser: http://YOUR_IP:8000

Example: http://192.168.1.100:8000

🔧 Troubleshooting
--> Camera not working?
# Try different camera index
# Edit realtime_predict.py line 35: cv2.VideoCapture(1)

-->Port already in use?
python manage.py runserver 0.0.0.0:8001

-->Dependencies missing?
pip install tensorflow opencv-python django pyttsx3 gtts pillow

# Folder Structure 

SignSpeak/
├── model/signspeak_model.h5        # AI model
├── realtime_predict.py             # Desktop app
├── requirements.txt                # Dependencies
├── webapp/                         # Web application
└── README.md                       # Documentation

