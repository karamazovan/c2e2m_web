from django import forms
from .models import Response, Question, Demographic, SurveyResponse

class ResponseForm(forms.ModelForm):
    CHOICES = [(1, 'Music 1'), (2, 'Music 2')]

    class Meta:
        model = Response
        fields = ['preferred_music']  # Use the correct field name from the Response model

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', None)
        super(ResponseForm, self).__init__(*args, **kwargs)
        if questions:
            for question in questions:
                field_name = f'question_{question.id}_preferred_music'
                self.fields[field_name] = forms.ChoiceField(
                    choices=self.CHOICES,
                    widget=forms.RadioSelect(),
                    label=question.text
                )

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

class DemographicForm(forms.ModelForm):
    class Meta:
        model = Demographic
        fields = ['age', 'gender', 'music_experience']
        widgets = {
            'colour_association': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }

class ViewingExperienceForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = [
            'colour_music_combination', 'visual_mood_rating', 'visual_emotions',
            'music_visual_match', 'mood_change_soundtrack', 'soundtrack_mood_rating',
            'c2e2m_effectiveness', 'c2e2m_improvements', 'additional_feedback'
        ]
        widgets = {
            'visual_emotions': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'mood_change_soundtrack': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'c2e2m_improvements': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'additional_feedback': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }
