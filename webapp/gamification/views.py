from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import date, timedelta
from .models import *
from authentication.models import UserProfile
import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    profile = user.userprofile
    
    # Get recent sessions
    recent_sessions = GameSession.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get achievements
    user_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')
    
    # Get skill tree progress
    skill_progress = UserProgress.objects.filter(user=user).select_related('skill_tree')
    
    # Calculate weekly XP
    week_ago = timezone.now() - timedelta(days=7)
    weekly_xp = sum([session.xp_earned for session in GameSession.objects.filter(
        user=user, created_at__gte=week_ago
    )])
    
    return Response({
        'user_stats': {
            'level': profile.level,
            'xp_points': profile.xp_points,
            'current_streak': profile.current_streak,
            'longest_streak': profile.longest_streak,
            'weekly_xp': weekly_xp
        },
        'recent_sessions': [{
            'game_mode': session.game_mode,
            'score': session.score,
            'accuracy': session.accuracy,
            'xp_earned': session.xp_earned,
            'date': session.created_at.strftime('%Y-%m-%d')
        } for session in recent_sessions],
        'achievements': [{
            'name': ua.achievement.name,
            'description': ua.achievement.description,
            'icon': ua.achievement.icon,
            'earned_date': ua.earned_date.strftime('%Y-%m-%d')
        } for ua in user_achievements],
        'skill_progress': [{
            'skill_name': sp.skill_tree.name,
            'skill_type': sp.skill_tree.skill_type,
            'progress': sp.progress_percentage,
            'completed': sp.completed
        } for sp in skill_progress]
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_game(request):
    game_mode = request.data.get('game_mode')
    
    if game_mode == 'sign_race':
        # Generate random letters for sign race
        letters = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 10)
        return Response({
            'game_id': f"race_{timezone.now().timestamp()}",
            'challenge': letters,
            'time_limit': 60,
            'instructions': 'Sign each letter as fast as you can!'
        })
    
    elif game_mode == 'memory_match':
        # Generate word for memory match
        words = ['CAT', 'DOG', 'HELLO', 'WORLD', 'LOVE', 'FAMILY']
        word = random.choice(words)
        return Response({
            'game_id': f"memory_{timezone.now().timestamp()}",
            'word': word,
            'letters': list(word),
            'instructions': f'Sign each letter of "{word}" in order'
        })
    
    elif game_mode == 'daily_challenge':
        # Get today's challenge
        today_challenge = DailyChallenge.objects.filter(date=date.today()).first()
        if not today_challenge:
            # Create default challenge if none exists
            today_challenge = DailyChallenge.objects.create(
                challenge_type='animals',
                title='Sign 5 Animals',
                description='Practice signing these animal names',
                target_signs=['CAT', 'DOG', 'BIRD', 'FISH', 'HORSE'],
                xp_reward=200
            )
        
        return Response({
            'game_id': f"daily_{today_challenge.id}",
            'title': today_challenge.title,
            'description': today_challenge.description,
            'target_signs': today_challenge.target_signs,
            'xp_reward': today_challenge.xp_reward
        })
    
    return Response({'error': 'Invalid game mode'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_score(request):
    user = request.user
    profile = user.userprofile
    
    game_mode = request.data.get('game_mode')
    score = request.data.get('score', 0)
    accuracy = request.data.get('accuracy', 0.0)
    time_taken = request.data.get('time_taken', 0)
    
    # Calculate XP based on performance
    base_xp = 50
    accuracy_bonus = int(accuracy * 50)  # Up to 50 bonus XP for 100% accuracy
    speed_bonus = max(0, 30 - time_taken // 2)  # Bonus for speed
    
    xp_earned = base_xp + accuracy_bonus + speed_bonus
    
    # Create game session
    session = GameSession.objects.create(
        user=user,
        game_mode=game_mode,
        score=score,
        accuracy=accuracy,
        time_taken=time_taken,
        xp_earned=xp_earned
    )
    
    # Add XP to user profile
    profile.add_xp(xp_earned)
    
    # Update streak
    today = date.today()
    if profile.last_practice_date == today - timedelta(days=1):
        profile.current_streak += 1
    elif profile.last_practice_date != today:
        profile.current_streak = 1
    
    if profile.current_streak > profile.longest_streak:
        profile.longest_streak = profile.current_streak
    
    profile.last_practice_date = today
    profile.save()
    
    # Check for achievements
    check_achievements(user, session)
    
    return Response({
        'xp_earned': xp_earned,
        'total_xp': profile.xp_points,
        'level': profile.level,
        'current_streak': profile.current_streak,
        'session_id': session.id
    })

def check_achievements(user, session):
    profile = user.userprofile
    
    # Speed Signer achievement
    if session.game_mode == 'sign_race' and session.time_taken < 30:
        achievement, created = Achievement.objects.get_or_create(
            badge_type='speed_signer',
            defaults={
                'name': 'Speed Signer',
                'description': 'Complete Sign Race in under 30 seconds',
                'requirement': {'time_limit': 30},
                'icon': '⚡'
            }
        )
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)
    
    # Perfect Week achievement
    if profile.current_streak >= 7:
        achievement, created = Achievement.objects.get_or_create(
            badge_type='perfect_week',
            defaults={
                'name': 'Perfect Week',
                'description': 'Practice for 7 days in a row',
                'requirement': {'streak': 7},
                'icon': '🔥'
            }
        )
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    period = request.GET.get('period', 'weekly')
    
    # Calculate leaderboard based on period
    if period == 'weekly':
        week_ago = timezone.now() - timedelta(days=7)
        users_xp = {}
        sessions = GameSession.objects.filter(created_at__gte=week_ago)
        
        for session in sessions:
            if session.user.id not in users_xp:
                users_xp[session.user.id] = {
                    'user': session.user,
                    'total_xp': 0
                }
            users_xp[session.user.id]['total_xp'] += session.xp_earned
        
        # Sort by XP
        leaderboard_data = sorted(users_xp.values(), key=lambda x: x['total_xp'], reverse=True)[:10]
        
        return Response([{
            'rank': idx + 1,
            'username': data['user'].username,
            'total_xp': data['total_xp'],
            'level': data['user'].userprofile.level
        } for idx, data in enumerate(leaderboard_data)])
    
    return Response({'error': 'Invalid period'}, status=status.HTTP_400_BAD_REQUEST)