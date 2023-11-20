# duck_code_editor/views.py
import subprocess
import json
import regex as re
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .forms import CodeSnippetForm
from .models import Trial_Task, Trial
from django.utils import timezone


def code_editor(request, task_number):
    # Retrieve the study_id from the session
    selected_study_id = request.session.get('selected_study_id')

    print(f'study_id: {selected_study_id}, task_number: {task_number}')

    with open('tasks/task_assignment.json', 'r') as assignment_file:
        study_assignment = json.load(assignment_file)

    # Get the task set associated with the study ID, defaulting to 'default_task_set' if not found
    task_set_name = study_assignment.get(selected_study_id)
    task_test = load_tasks(f'tasks/{task_set_name}.json')

    # Validate that the task_number is a non-negative integer
    try:
        task_number = int(task_number)
        if task_number < 0 or task_number >= len(task_test) + 1:
            raise ValueError("Invalid task number")
    except ValueError:
        return HttpResponseBadRequest("Invalid task number")

    output = None
    try:
        current_task = task_test[task_number]
    except IndexError:
        return redirect('duck_code_editor:break_page')

    if request.method == 'POST':
        # Check if 'Next Task' button is pressed
        if 'next' in request.POST:

            # safe time and solution in trial_task instance
            # current_task_instance = Trial_Task.objects.get(
            current_trial = Trial.objects.get(
                student_id=selected_study_id,
            )
            if task_number == 0:
                trial_task = current_trial.task_1

            elif task_number == 1:
                trial_task = current_trial.task_2

            elif task_number == 2:
                trial_task = current_trial.task_3
            trial_task.end_time = timezone.now()
            trial_task.duration = trial_task.end_time - trial_task.start_time
            trial_task.student_solution = request.POST.get('code')
            trial_task.save()

            # Redirect to the next task with its number in the URL
            return redirect('duck_code_editor:feedback', task_number=task_number)

        elif 'run_code' in request.POST:

            print('run_code')
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

    # Initialize the form with the code from the current task
    else:
        form = CodeSnippetForm(
            initial={'code': current_task.get('code_to_debug', '')})
        current_task_instance = Trial_Task.objects.create(
            task_name=current_task['title'],
            start_time=timezone.now(),
            solved_with_duck=False
        )

        # If it's first task, create a new trial instance
        if task_number == 0:
            # Create a new task instance and set 'start_time'
            Trial.objects.create(
                student_id=selected_study_id,
                group=task_set_name,
                task_1=current_task_instance,
            )
        else:
            current_trial = Trial.objects.get(
                student_id=selected_study_id)

            if task_number == 1:
                current_trial.task_2 = current_task_instance
            elif task_number == 2:
                current_trial.task_3 = current_task_instance
            else:
                breakpoint()

            current_trial.save()

    return render(request, 'duck_code_editor/code_editor.html', {
        'form': form,
        'task_number': task_number+1,
        'output': output,
        'current_task': current_task,
        'duck': False,
    })


def code_editor_duck(request, task_number):
    # Retrieve the study_id from the session
    selected_study_id = request.session.get('selected_study_id')
    print(f'study_id: {selected_study_id}, task_number: {task_number}')

    with open('tasks/task_assignment.json', 'r') as assignment_file:
        study_assignment = json.load(assignment_file)

    # Get the task set associated with the study ID, defaulting to 'default_task_set' if not found
    task_set_name = study_assignment.get(selected_study_id)
    # take the other task set
    if task_set_name == 'task_set_a':
        task_set_name = 'task_set_b'
    else:
        task_set_name = 'task_set_a'
    task_set = load_tasks(f'tasks/{task_set_name}.json')

    # Validate that the task_number is a non-negative integer
    try:
        task_number = int(task_number)
        if task_number < 0 or task_number >= len(task_set) + 1:
            raise ValueError("Invalid task number")
    except ValueError:
        return HttpResponseBadRequest("Invalid task number")

    try:
        current_task = task_set[task_number]
    except IndexError:
        return redirect('duck_code_editor:survey')

    output = None

    if request.method == 'POST':
        # Check if 'Next Task' button is pressed
        if 'next' in request.POST:
            # If 'Next Task' button is pressed, increment the task number
            # safe time and solution in trial_task instance
            # current_task_instance = Trial_Task.objects.get(
            current_trial = Trial.objects.get(
                student_id=selected_study_id,
            )
            if task_number == 0:
                trial_task = current_trial.task_1_duck

            elif task_number == 1:
                trial_task = current_trial.task_2_duck

            elif task_number == 2:
                trial_task = current_trial.task_3_duck

            trial_task.end_time = timezone.now()
            trial_task.duration = trial_task.end_time - trial_task.start_time
            trial_task.student_solution = request.POST.get('code')
            trial_task.save()
            # Redirect to the next task with its number in the URL
            return redirect('duck_code_editor:feedback_duck', task_number=task_number)

        elif 'run_code' in request.POST:
            print('run_code')
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
            form = CodeSnippetForm(
                initial={'code': current_task.get('code_to_debug', '')})

            # Create a new task instance and set 'start_time'
            current_task_instance = Trial_Task.objects.create(
                task_name=current_task['title'],
                start_time=timezone.now(),
                solved_with_duck=True
            )

            current_trial = Trial.objects.get(
                student_id=selected_study_id)
            
            current_trial.task_1_duck = current_task_instance

            current_trial.save()
    else:
        # Initialize the form with the code from the current task
        form = CodeSnippetForm(
            initial={'code': current_task.get('code_to_debug', '')})

        # Create a new task instance and set 'start_time'
        current_task_instance = Trial_Task.objects.create(
            task_name=current_task['title'],
            start_time=timezone.now(),
            solved_with_duck=True
        )
        current_trial = Trial.objects.get(
            student_id=selected_study_id)
      
        if task_number == 1:
            current_trial.task_2_duck = current_task_instance
        elif task_number == 2:
            current_trial.task_3_duck = current_task_instance
        else:
            breakpoint()

        current_trial.save()

    return render(request, 'duck_code_editor/code_editor.html', {
        'form': form,
        'task_number': task_number+1,
        'output': output,
        'current_task': current_task,
        'duck': True,
    })


def survey_complete(request):
    return render(request, 'duck_code_editor/survey_complete.html')


def execute_code(code):
    try:
        # Use subprocess to run the code in a separate process
        result = subprocess.check_output(
            ["python", "-c", code], stderr=subprocess.STDOUT, text=True)
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


def start_experiment(request):
    if request.method == 'POST':
        selected_study_id = request.POST.get('study_id')
        if selected_study_id:
            # Store the study_id in the session
            request.session['selected_study_id'] = selected_study_id
            # Redirect to code_editor view without including study_id in the URL
            return redirect('duck_code_editor:code_editor', task_number=0)

    return render(request, 'duck_code_editor/start_experiment.html')


def break_page(request):
    return render(request, 'duck_code_editor/break.html')


def instructions(request):
    return render(request, 'duck_code_editor/instructions.html')


def rubber_duck_instructions(request):
    return render(request, 'duck_code_editor/rubber_duck_instructions.html')


def feedback(request, task_number):
    selected_study_id = request.session.get('selected_study_id')
    current_trial = Trial.objects.get(student_id=selected_study_id)

    if request.method == 'POST':
        # depending on whether duck is in the URL as in task<nr>duck, redirect to the correct URL
        regex_pattern = re.compile(r'task\d+duck')
        duck_debugging = regex_pattern.search(request.path)

        if task_number == 0:
            current_trial_task = current_trial.task_1
            if duck_debugging:
                current_trial_task = current_trial.task_1_duck
        elif task_number == 1:
            current_trial_task = current_trial.task_2
            if duck_debugging:
                current_trial_task = current_trial.task_2_duck
        elif task_number == 2:
            current_trial_task = current_trial.task_3
            if duck_debugging:
                current_trial_task = current_trial.task_3_duck
        else:
            return HttpResponseBadRequest("Invalid task number")

        # Save the perceived complexity from the form submission
        perceived_complexity = request.POST.get('complexity')
        if perceived_complexity:
            current_trial_task.perceived_complexity = perceived_complexity
            current_trial_task.save()

        if duck_debugging:
            return redirect('duck_code_editor:code_editor_duck', task_number=task_number+1)
        else:
            return redirect('duck_code_editor:code_editor', task_number=task_number+1)

    return render(request, 'duck_code_editor/complexity_feedback.html')


def survey(request):
    if request.method == 'POST':
        # Save survey responses to the database
        survey_q1 = request.POST.get('survey_q1')
        survey_q2 = request.POST.get('survey_q2')

        trial = Trial.objects.get(
            student_id=request.session.get('selected_study_id'))
        
        # Save to your model instance (replace YourModel with the actual name of your model)
        trial.survey_q1 = survey_q1
        trial.survey_q2 = survey_q2 
        
        trial.save()
        
        return redirect('duck_code_editor:survey_complete')

    return render(request, 'duck_code_editor/survey.html')