from django import forms
from .models import CodeSnippet
from django_ace import AceWidget

class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['code']
        widgets = {
            'code': AceWidget(mode='python', theme='twilight'),
        }