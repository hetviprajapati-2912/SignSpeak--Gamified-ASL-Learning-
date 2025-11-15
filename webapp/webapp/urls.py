from django.contrib import admin
from django.urls import path, include
from predictapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main application routes
    path('', views.auth_page, name='auth_page'),
    path('auth/', views.auth_page, name='auth_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('sign-race/', views.sign_race_game, name='sign_race_game'),
    path('memory-match/', views.memory_match_game, name='memory_match_game'),
    path('daily-learning/', views.daily_learning, name='daily_learning'),
    path('learn/alphabets/', views.learn_alphabets, name='learn_alphabets'),
    path('learn/numbers/', views.learn_numbers, name='learn_numbers'),  # Numbers learning page
    path('learn/animals/', views.learn_animals, name='learn_animals'),  # Animals learning page
    path('learn/food/', views.learn_food, name='learn_food'),  # Food & Drinks learning page
    path('learn/greetings/', views.learn_greetings, name='learn_greetings'),  # Greetings page
    path('learn/emotions/', views.learn_emotions, name='learn_emotions'),  # Emotions page
    path('learn/relations/', views.learn_relations, name='learn_relations'),  # Family Relations page
    path('about/', views.about_page, name='about_page'),  # About page
    path('predict/', views.predict_image, name='predict_image'),
    path('webcam/', views.predict_from_webcam, name='predict_webcam'),
    path('start-camera-script/', views.start_camera_script, name='start_camera_script'),
    
    # API Routes
    path('api/auth/', include('authentication.urls')),
    path('api/gamification/', include('gamification.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)