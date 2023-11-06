from django.urls import path
from .views import code_editor

app_name = 'duck_code_editor'

urlpatterns = [
    path('code-editor/', code_editor, name='code_editor'),
]