# duck_code_editor/views.py
import subprocess
import json
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .forms import CodeSnippetForm

def code_editor(request, task_number):
    # Load all tasks from task_set_a.json
    task_set_a = load_tasks('tasks/task_set_a.json')

    # Validate that the task_number is a non-negative integer
    try:
        task_number = int(task_number)
        if task_number < 0 or task_number >= len(task_set_a):
            raise ValueError("Invalid task number")
    except ValueError:
        return HttpResponseBadRequest("Invalid task number")

    current_task = task_set_a[task_number]
    output = None
    
    if request.method == 'POST':
        # Check if 'Next Task' button is pressed
        if 'next_task' in request.POST:
            # If 'Next Task' button is pressed, increment the task number
            next_task_number = task_number + 1

            # If we've reached the end of tasks, redirect to the survey completion page
            if next_task_number >= len(task_set_a):
                return redirect('duck_code_editor:survey_complete')  # Use the correct URL name

            # Redirect to the next task with its number in the URL
            return redirect('duck_code_editor:code_editor', task_number=next_task_number)

        elif 'run_code' in request.POST:
            # If 'Run Code' button is pressed, execute the code
            form = CodeSnippetForm(request.POST)
            if form.is_valid():
                code_snippet = form.save()
                try:
                    output = execute_code(code_snippet.code)
                except Exception as e:
                    output = f"Error: {e}"
            else:
                output = None
    else: 
        # Initialize the form with the code from the current task
        form = CodeSnippetForm(initial={'code': current_task.get('code_to_debug', '')})


    return render(request, 'duck_code_editor/code_editor.html', {
        'form': form,
        'output': output,
        'current_task': current_task,
        
    })

# The rest of your code remains unchanged

def survey_complete(request):
    return render(request, 'duck_code_editor/survey_complete.html')

def execute_code(code):
    try:
        # Use subprocess to run the code in a separate process
        result = subprocess.check_output(["python", "-c", code], stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        # Handle errors, if any
        return f"Error: {e.output.strip()}"

def load_tasks(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            tasks = json.load(file)
        return tasks
    except FileNotFoundError:
        return []  # Return an empty list if the file is not found or cannot be read
    except json.JSONDecodeError:
        return []  # Return an empty list if there's an issue decoding the JSON