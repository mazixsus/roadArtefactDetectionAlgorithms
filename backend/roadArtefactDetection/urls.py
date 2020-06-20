from django.conf.urls import url
from . import views


urlpatterns = [
    url('survey/names', views.get_survey_names, name='get_survey_name'),
    url('survey/results', views.get_results, name='get_results'),
    url('survey/add', views.add_survey, name='add_survey'),
]
