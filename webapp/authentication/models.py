from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Gamification fields
    xp_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_practice_date = models.DateField(null=True, blank=True)
    
    # Progress tracking
    letters_mastered = models.JSONField(default=list)
    words_mastered = models.JSONField(default=list)
    phrases_mastered = models.JSONField(default=list)
    
    # Achievements
    badges_earned = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level}"
    
    def add_xp(self, points):
        self.xp_points += points
        # Level up every 1000 XP
        new_level = (self.xp_points // 1000) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
