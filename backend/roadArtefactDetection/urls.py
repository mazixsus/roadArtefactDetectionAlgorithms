from django.conf.urls import url
from . import views


urlpatterns = [
    url('new', views.new_view, name='new_view'),
    url('survey/names', views.get_survey_names, name='get_survey_name'),
    url('survey/results', views.get_results, name='get_results'),
    url('survey/bumps', views.get_bumps, name='get_bumps'),
]
