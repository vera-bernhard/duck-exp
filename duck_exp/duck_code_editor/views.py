# duck_code_editor/views.py
import subprocess
from django.shortcuts import render, redirect
from .forms import CodeSnippetForm

def code_editor(request):
    output = None

    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            code_snippet = form.save()

            # Execute the code using subprocess
            try:
                output = execute_code(code_snippet.code)
            except Exception as e:
                output = f"Error: {e}"

    else:
        form = CodeSnippetForm()

    return render(request, 'duck_code_editor/code_editor.html', {'form': form, 'output': output})

def execute_code(code):
    try:
        # Use subprocess to run the code in a separate process
        result = subprocess.check_output(["python", "-c", code], stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        # Handle errors, if any
        return f"Error: {e.output.strip()}"
