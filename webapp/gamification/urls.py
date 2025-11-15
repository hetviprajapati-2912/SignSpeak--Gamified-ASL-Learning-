from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start-game/', views.start_game, name='start_game'),
    path('submit-score/', views.submit_score, name='submit_score'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]