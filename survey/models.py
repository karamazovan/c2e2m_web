from django.db import models
from django.core.exceptions import ValidationError

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
    preferred_music = models.IntegerField(choices=[(1, 'Music 1'), (2, 'Music 2')], null=True, validators=[validate_preferred_music])

    def __str__(self):
        return f"Survey {self.survey.id} response: Preferred music {self.preferred_music}"