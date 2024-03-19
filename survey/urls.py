from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('<int:survey_id>/', views.survey_detail_view, name='detail'),
    path('<int:survey_id>/vote/', views.vote, name='vote'),
    path('<int:survey_id>/results/', views.survey_results, name='results'),
    path('thank_you/', views.thank_you_view, name='thank_you'),
]
