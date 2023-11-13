# duck_code_editor/urls.py
from django.urls import path
from .views import code_editor, survey_complete, start_experiment

app_name = 'duck_code_editor'

urlpatterns = [
    path('code-editor/<int:task_number>/', code_editor, name='code_editor'),
    path('survey-complete/', survey_complete, name='survey_complete'),
    path('', start_experiment, name='start_experiment'),  # Make start_experiment the default view
]
