from django.shortcuts import render, redirect, get_object_or_404
from .models import Survey
from .forms import SurveyForm

def survey_view(request):
    survey_id = 1
    survey_name = get_object_or_404(Survey, pk=survey_id).title
    return render(request, 'survey/survey.html', {'survey_id': survey_id, 'survey_name': survey_name})

def survey_detail_view(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    return render(request, 'survey/survey_detail.html', {'survey': survey})

def vote(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    try:
        selected_choice = request.POST['music_choice']
    except (KeyError, ValueError):
        # Redisplay the survey voting form.
        return render(request, 'survey/survey_detail.html', {
            'survey': survey,
            'error_message': "You didn't select a choice.",
        })
    else:
        response = Response(survey=survey, preferred_music=selected_choice)
        response.save()
        # Redirect to a new URL to prevent double posting:
        return redirect('survey_results', survey_id=survey.id)

def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    responses = Response.objects.filter(survey=survey)
    return render(request, 'survey/vote.html', {'survey': survey, 'responses': responses})

def thank_you_view(request):
    return render(request, 'survey/thank_you.html')
