from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_iteration = models.IntegerField(default=1)
    last_completed_survey = models.IntegerField(default=0)
    current_vote_count = models.IntegerField(default=0)
    stage = models.CharField(max_length=30, default='demographic')

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Demographic(models.Model):
    AGE_CHOICES = [
        ('18-24', '18 to 24'),
        ('25-34', '25 to 34'),
        ('35-44', '35 to 44'),
        ('45-54', '45 to 54'),
        ('55-64', '55 to 64'),
        ('65+', '65 or over'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Prefer not to say'),
    ]

    MUSIC_EXPERIENCE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=5, choices=AGE_CHOICES)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    music_experience = models.CharField(max_length=3, choices=MUSIC_EXPERIENCE_CHOICES)


    def __str__(self):
        return f"Demographics for {self.user.username}"

class Survey(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='surveys/images/', null=True, blank=True)
    music_file_1 = models.FileField(upload_to='surveys/music/', null=True, blank=True)
    music_file_2 = models.FileField(upload_to='surveys/music/', null=True, blank=True)

    def __str__(self):
        return self.title

def validate_preferred_music(value):
    print(f"Validating preferred_music: {value}")
    if value not in [1, 2]:
        raise ValidationError(f"{value} is not a valid choice. Choose 1 or 2.")


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    preferred_music = models.IntegerField(choices=[(1, 'Music 1'), (2, 'Music 2')], null=True, validators=[validate_preferred_music])
    # 'choice' field is not needed if 'preferred_music' is the intended field.

    def __str__(self):
        user_username = self.user.username if self.user else 'Anonymous'
        return f"{user_username}'s response to {self.survey.title}: Preferred music {self.preferred_music}"

class SurveyResponse(models.Model):
    # Generate choices from 1 to 5
    MOOD_RATING_CHOICES = [(str(i), str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_mood = models.CharField(max_length=1, choices=MOOD_RATING_CHOICES)
    colour_association = models.TextField(verbose_name="a colour associated with happiness/sadness")
    music_mood_influence = models.CharField(max_length=1, choices=MOOD_RATING_CHOICES)

    # Viewing Experience related fields
    colour_music_combination = models.CharField(max_length=1, choices=MOOD_RATING_CHOICES)
    visual_mood_rating = models.CharField(max_length=1, choices=MOOD_RATING_CHOICES)
    visual_emotions = models.TextField(blank=True, null=True)
    music_visual_match = models.CharField(max_length=1, choices=MOOD_RATING_CHOICES)
    mood_change_soundtrack = models.TextField(blank=True, null=True)
    soundtrack_mood_rating = models.CharField(max_length=1, choices=MOOD_RATING_CHOICES)
    c2e2m_effectiveness = models.CharField(max_length=1, choices=MOOD_RATING_CHOICES)
    c2e2m_improvements = models.TextField(blank=True, null=True)
    additional_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Viewing Experience for {self.user.username}"
