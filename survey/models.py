from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_iteration = models.IntegerField(default=1)
    last_completed_survey = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Survey(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='surveys/images/', null=True, blank=True)
    music_file_1 = models.FileField(upload_to='surveys/music/', null=True, blank=True)
    music_file_2 = models.FileField(upload_to='surveys/music/', null=True, blank=True)

    def __str__(self):
        return self.title

def validate_preferred_music(value):
    if value not in [1, 2]:
        raise ValidationError(f"{value} is not a valid choice. Choose 1 or 2.")

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='responses')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    preferred_music = models.IntegerField(choices=[(1, 'Music 1'), (2, 'Music 2')], null=True, validators=[validate_preferred_music])

    def __str__(self):
        user_username = self.user.username if self.user else 'Anonymous'
        return f"{user_username}'s response to {self.survey.title}: Preferred music {self.preferred_music}"
