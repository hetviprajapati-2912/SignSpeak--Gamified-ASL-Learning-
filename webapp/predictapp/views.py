import base64
import io
import numpy as np
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from keras.models import load_model
from PIL import Image
import os
import pyttsx3
from django.core.files.storage import FileSystemStorage

def auth_page(request):
    return render(request, 'predictapp/auth_enhanced.html')

def dashboard_page(request):
    return render(request, 'predictapp/dashboard_enhanced.html')

def sign_race_game(request):
    return render(request, 'predictapp/sign_race_game.html')

def memory_match_game(request):
    return render(request, 'predictapp/memory_match_game.html')

def daily_learning(request):
    return render(request, 'predictapp/daily_learning.html')

def learn_alphabets(request):
    return render(request, 'predictapp/learn_alphabets.html')

def learn_numbers(request):
    return render(request, 'predictapp/learn_numbers.html')

def learn_animals(request):
    return render(request, 'predictapp/learn_animals.html')

def learn_food(request):
    return render(request, 'predictapp/learn_food.html')

def learn_greetings(request):
    return render(request, 'predictapp/learn_greetings.html')

def learn_emotions(request):
    return render(request, 'predictapp/learn_emotions.html')

def learn_relations(request):
    return render(request, 'predictapp/learn_relations.html')

def about_page(request):
    return render(request, 'predictapp/about.html')

# Load trained model
model = load_model("model/signspeak_model.h5")

# Class labels
class_names = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'del', 'nothing', 'space'
]

# Predict from image upload via form (gesture image)
def predict_image(request):
    prediction = None
    uploaded_image_url = None

    if request.method == 'POST' and request.FILES.get('gesture'):
        image_file = request.FILES['gesture']
        image = Image.open(image_file).convert('L')
        image = image.resize((64, 64))
        img_array = np.array(image) / 255.0
        img_array = img_array.reshape(1, 64, 64, 1)

        pred = model.predict(img_array)
        predicted_class = class_names[np.argmax(pred)]
        prediction = predicted_class

        # Save uploaded image
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_image_url = fs.url(filename)

        # Optional: Text-to-Speech
        engine = pyttsx3.init()
        engine.say(f"The predicted sign is {predicted_class}")
        engine.runAndWait()

    return render(request, 'predictapp/model_enhanced.html', {
        'prediction': prediction,
        'uploaded_image_url': uploaded_image_url
    })

# Predict from webcam (base64 image)
@csrf_exempt
def predict_from_webcam(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(io.BytesIO(image_data)).convert('L')
        image = image.resize((64, 64))
        img_array = np.array(image) / 255.0
        img_array = img_array.reshape(1, 64, 64, 1)

        pred = model.predict(img_array)
        predicted_class = class_names[np.argmax(pred)]
        return JsonResponse({'prediction': predicted_class})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Launch external camera script
def start_camera_script(request):
    os.system("start cmd /k python realtime_predict.py")
    return HttpResponse("Started camera script.")