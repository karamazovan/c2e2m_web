from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Survey, Response, UserProfile, Question, Demographic, SurveyResponse
from .forms import VoteForm, ResponseForm, DemographicForm, ViewingExperienceForm
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
def demographic_survey(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    try:
        demographic = Demographic.objects.get(user=request.user)
    except Demographic.DoesNotExist:
        demographic = None

    if request.method == 'POST':
        form = DemographicForm(request.POST, instance=demographic)
        if form.is_valid():
            demographic = form.save(commit=False)
            demographic.user = request.user
            demographic.save()
            return HttpResponseRedirect(reverse('survey:detail', args=(6,)))
    else:
        form = DemographicForm(instance=demographic)

    return render(request, 'survey/demographic_survey.html', {'form': form})

@login_required
def vote(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    questions = list(survey.questions.all())
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ResponseForm(request.POST, questions=questions)
        if form.is_valid():
            response = form.save(commit=False)
            response.survey = survey
            response.user = request.user
            response.save()
            for question in questions:
                field_name = f'question_{question.id}_preferred_music'
                preferred_music = form.cleaned_data.get(field_name)
                print(f"Attempting to save Response for Question ID: {question.id}, Preferred Music: {preferred_music}")

                # Try-except block to catch and print any exceptions during Response object creation
                try:
                    response = Response.objects.create(
                        survey=survey,
                        user=request.user,
                        question=question,
                        preferred_music=preferred_music
                    )
                    print(f"Response saved: {response.id}")
                except Exception as e:
                    print(f"Error saving response for question {question.id}: {e}")
                    # Optionally, handle the error more gracefully here

            user_profile.current_iteration += 1
            user_profile.save()

            # Redirect to the next survey or a thank you page
            if survey_id == 41:  # Assuming 29 is the last survey ID
                if user_profile.current_iteration >= 40:
                    return HttpResponseRedirect(reverse('survey:viewing_experience'))
                else:
                    next_survey_id = 1
                    return HttpResponseRedirect(reverse('survey:detail', args=(next_survey_id,)))
            else:
                next_survey_id = survey_id + 1
                return HttpResponseRedirect(reverse('survey:detail', args=(next_survey_id,)))
        else:
            print("Form errors:", form.errors)
            return render(request, 'survey/vote.html',
                          {'survey': survey, 'form': form, 'error_message': "Form is not valid."})
    else:
        form = VoteForm(questions=questions)
        return render(request, 'survey/vote.html', {'survey': survey, 'form': form})

@login_required
def viewing_experience(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ViewingExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()

            user_profile.stage = 'completed'
            user_profile.save()

            return redirect('survey:thank_you')
    else:
        form = ViewingExperienceForm()
    return render(request, 'survey/viewing_experience.html', {'form': form})

def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    responses = Response.objects.filter(survey=survey)
    return render(request, 'survey/results.html', {'survey': survey, 'responses': responses})

def thank_you_view(request):
    return render(request, 'survey/thank_you.html')
