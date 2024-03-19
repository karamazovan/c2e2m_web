from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Survey, Response
from .forms import VoteForm
from django.contrib.auth.decorators import login_required

def index_view(request):
    surveys = Survey.objects.all()
    return render(request, 'survey/index.html', {'surveys': surveys})

def survey_detail_view(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    next_survey_id = survey.id + 1
    next_survey_exists = Survey.objects.filter(id=next_survey_id).exists()
    return render(request, 'survey/detail.html', {'survey': survey, 'next_survey_exists': next_survey_exists, 'next_survey_id': next_survey_id})

@login_required
def vote(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.survey = survey
            response.user = request.user
            response.save()

            next_survey_id = survey_id + 1
            next_survey_exists = Survey.objects.filter(pk=next_survey_id).exists()

            if next_survey_exists:
                return HttpResponseRedirect(reverse('survey:detail', args=(next_survey_id,)))
            else:
                return redirect('survey:thank_you')
        else:
            return render(request, 'survey/detail.html', {'survey': survey, 'form': form, 'error_message': "You didn't select a valid choice."})
    else:
        form = VoteForm()
    return render(request, 'survey/vote.html', {'survey': survey, 'form': form})

def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    responses = Response.objects.filter(survey=survey)
    return render(request, 'survey/results.html', {'survey': survey, 'responses': responses})

def thank_you_view(request):
    return render(request, 'survey/thank_you.html')
