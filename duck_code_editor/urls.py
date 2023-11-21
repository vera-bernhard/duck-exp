from django.urls import path
from .views import code_editor, code_editor_duck, without_duck_instructions,survey_complete, start_experiment, instructions, feedback, survey, rubber_duck_instructions, break_page

app_name = 'duck_code_editor'

urlpatterns = [
    path('', start_experiment, name='start_experiment'),
    path('task<int:task_number>/', code_editor, name='code_editor'),
    path('task<int:task_number>duck/', code_editor_duck, name='code_editor_duck'),
    path('task<int:task_number>/feedback/', feedback, name='feedback'),
    path('task<int:task_number>duck/feedback/', feedback, name='feedback_duck'),
    path('survey-complete/', survey_complete, name='survey_complete'),
    path('instructions/', instructions, name='instructions'),
    path('instructions-duck/', rubber_duck_instructions,
         name='rubber_duck_instructions'),
    path('without-instructions/', without_duck_instructions, name='without_instructions'),
    path('break/', break_page, name='break_page'),
    path('survey', survey, name='survey')
]
