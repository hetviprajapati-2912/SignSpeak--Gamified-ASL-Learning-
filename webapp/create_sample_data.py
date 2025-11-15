import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

from gamification.models import SkillTree, Achievement, DailyChallenge
from datetime import date

def create_sample_data():
    # Create Skill Trees
    skill_trees = [
        {
            'name': 'Basic Letters A-M',
            'skill_type': 'letters',
            'required_level': 1,
            'xp_reward': 100,
            'content': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
        },
        {
            'name': 'Advanced Letters N-Z',
            'skill_type': 'letters',
            'required_level': 2,
            'xp_reward': 150,
            'content': ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        },
        {
            'name': 'Common Words',
            'skill_type': 'words',
            'required_level': 3,
            'xp_reward': 200,
            'content': ['HELLO', 'WORLD', 'LOVE', 'FAMILY', 'FRIEND', 'THANK', 'YOU']
        },
        {
            'name': 'Basic Phrases',
            'skill_type': 'phrases',
            'required_level': 5,
            'xp_reward': 300,
            'content': ['HOW ARE YOU', 'NICE TO MEET YOU', 'WHAT IS YOUR NAME']
        }
    ]
    
    for skill_data in skill_trees:
        skill, created = SkillTree.objects.get_or_create(
            name=skill_data['name'],
            defaults=skill_data
        )
        if created:
            print(f"Created skill tree: {skill.name}")
    
    # Create Achievements
    achievements = [
        {
            'name': 'Speed Signer',
            'badge_type': 'speed_signer',
            'description': 'Complete Sign Race in under 30 seconds',
            'requirement': {'time_limit': 30, 'game_mode': 'sign_race'},
            'xp_reward': 100,
            'icon': '⚡'
        },
        {
            'name': 'Perfect Week',
            'badge_type': 'perfect_week',
            'description': 'Practice for 7 days in a row',
            'requirement': {'streak': 7},
            'xp_reward': 200,
            'icon': '🔥'
        },
        {
            'name': 'Conversation Master',
            'badge_type': 'conversation_master',
            'description': 'Complete 10 conversation challenges',
            'requirement': {'conversations_completed': 10},
            'xp_reward': 300,
            'icon': '💬'
        },
        {
            'name': 'Streak Master',
            'badge_type': 'streak_master',
            'description': 'Achieve a 30-day practice streak',
            'requirement': {'streak': 30},
            'xp_reward': 500,
            'icon': '🏆'
        },
        {
            'name': 'Daily Champion',
            'badge_type': 'daily_champion',
            'description': 'Complete 50 daily challenges',
            'requirement': {'daily_challenges': 50},
            'xp_reward': 250,
            'icon': '🌟'
        }
    ]
    
    for achievement_data in achievements:
        achievement, created = Achievement.objects.get_or_create(
            badge_type=achievement_data['badge_type'],
            defaults=achievement_data
        )
        if created:
            print(f"Created achievement: {achievement.name}")
    
    # Create Daily Challenges
    daily_challenges = [
        {
            'challenge_type': 'animals',
            'title': 'Sign 5 Animals',
            'description': 'Practice signing these animal names',
            'target_signs': ['CAT', 'DOG', 'BIRD', 'FISH', 'HORSE'],
            'xp_reward': 200,
            'date': date.today()
        },
        {
            'challenge_type': 'colors',
            'title': 'Sign 5 Colors',
            'description': 'Practice signing these color names',
            'target_signs': ['RED', 'BLUE', 'GREEN', 'YELLOW', 'BLACK'],
            'xp_reward': 200,
            'date': date.today()
        },
        {
            'challenge_type': 'numbers',
            'title': 'Sign Numbers 1-10',
            'description': 'Practice signing numbers from 1 to 10',
            'target_signs': ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN'],
            'xp_reward': 250,
            'date': date.today()
        }
    ]
    
    for challenge_data in daily_challenges:
        challenge, created = DailyChallenge.objects.get_or_create(
            challenge_type=challenge_data['challenge_type'],
            date=challenge_data['date'],
            defaults=challenge_data
        )
        if created:
            print(f"Created daily challenge: {challenge.title}")

if __name__ == '__main__':
    create_sample_data()
    print("Sample data created successfully!")