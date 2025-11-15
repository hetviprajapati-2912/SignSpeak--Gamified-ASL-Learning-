from django.db import models
from django.contrib.auth.models import User
from datetime import date

class SkillTree(models.Model):
    SKILL_TYPES = [
        ('letters', 'Letters'),
        ('words', 'Words'),
        ('phrases', 'Phrases'),
        ('conversations', 'Conversations')
    ]
    
    name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES)
    required_level = models.IntegerField(default=1)
    xp_reward = models.IntegerField(default=50)
    content = models.JSONField(default=list)  # List of signs to learn
    
    def __str__(self):
        return f"{self.name} ({self.skill_type})"

class Achievement(models.Model):
    BADGE_TYPES = [
        ('speed_signer', 'Speed Signer'),
        ('perfect_week', 'Perfect Week'),
        ('conversation_master', 'Conversation Master'),
        ('streak_master', 'Streak Master'),
        ('daily_champion', 'Daily Champion')
    ]
    
    name = models.CharField(max_length=100)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    description = models.TextField()
    requirement = models.JSONField()  # Conditions to unlock
    xp_reward = models.IntegerField(default=100)
    icon = models.CharField(max_length=50, default='🏆')
    
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement']

class GameSession(models.Model):
    GAME_MODES = [
        ('sign_race', 'Sign Race'),
        ('memory_match', 'Memory Match'),
        ('story_mode', 'Story Mode'),
        ('daily_challenge', 'Daily Challenge')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_mode = models.CharField(max_length=20, choices=GAME_MODES)
    score = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)
    time_taken = models.IntegerField(default=0)  # in seconds
    xp_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.game_mode} - {self.score}"

class DailyChallenge(models.Model):
    CHALLENGE_TYPES = [
        ('animals', 'Sign 5 Animals'),
        ('colors', 'Sign 5 Colors'),
        ('numbers', 'Sign Numbers 1-10'),
        ('family', 'Sign Family Members'),
        ('food', 'Sign 5 Foods')
    ]
    
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    target_signs = models.JSONField()  # List of signs to complete
    xp_reward = models.IntegerField(default=200)
    date = models.DateField(default=date.today)
    
    def __str__(self):
        return f"{self.title} - {self.date}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_tree = models.ForeignKey(SkillTree, on_delete=models.CASCADE)
    progress_percentage = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'skill_tree']

class Leaderboard(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all_time', 'All Time')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    total_xp = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'period']