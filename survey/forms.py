from django import forms
from .models import Response

class SurveyForm(forms.ModelForm):
    CHOICES = [('1', 'Music 1'), ('2', 'Music 2')]
    preferred_music = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Response
        fields = ['preferred_music']
class VoteForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['preferred_music']  # Update with the actual fields you need for voting
