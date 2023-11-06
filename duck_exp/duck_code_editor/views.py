from django.shortcuts import render

# Create your views here.

# duck_code_editor/views.py
from django.shortcuts import render, redirect
from .forms import CodeSnippetForm

def code_editor(request):
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('duck_code_editor:code_editor')
    else:
        form = CodeSnippetForm()

    return render(request, 'duck_code_editor/code_editor.html', {'form': form})

