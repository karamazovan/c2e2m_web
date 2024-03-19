from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_view, name='survey'),
    path('<int:pk>/', views.survey_detail_view, name='survey_detail'),
    path('thank_you/', views.thank_you_view, name='thank_you'),
]