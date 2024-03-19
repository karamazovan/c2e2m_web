from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Survey, Response, UserProfile
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
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.survey = survey
            response.user = request.user
            response.save()

            # 마지막 설문조사를 완료한 경우, 순환을 업데이트합니다.
            if survey_id == 5:
                user_profile.last_completed_survey = 0
                if user_profile.current_iteration < 4:
                    user_profile.current_iteration += 1
                    next_survey_id = 1  # 다음 순환의 첫 번째 설문조사로 리디렉트합니다.
                else:
                    # 모든 순환을 완료한 경우, 감사 페이지로 리디렉트합니다.
                    return redirect('survey:thank_you')
            else:
                user_profile.last_completed_survey = survey_id
                next_survey_id = survey_id + 1  # 다음 설문조사로 넘어갑니다.

            user_profile.save()
            return HttpResponseRedirect(reverse('survey:detail', args=(next_survey_id,)))
        else:
            # 폼이 유효하지 않으면 에러 메시지를 표시합니다.
            return render(request, 'survey/detail.html', {'survey': survey, 'form': form, 'error_message': "You didn't select a valid choice."})
    else:
        # GET 요청시 빈 폼을 제공합니다.
        form = VoteForm()
    return render(request, 'survey/vote.html', {'survey': survey, 'form': form})

def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    responses = Response.objects.filter(survey=survey)
    return render(request, 'survey/results.html', {'survey': survey, 'responses': responses})

def thank_you_view(request):
    return render(request, 'survey/thank_you.html')
