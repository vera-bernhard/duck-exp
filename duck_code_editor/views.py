# duck_code_editor/views.py
import json
import random
import subprocess
import signal

import regex as re
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import CodeSnippetForm
from .models import Trial, Trial_Task

NR_OF_TASKS = 3

TASK_SETS = ['task_set_a', 'task_set_b']


def code_editor(request, task_number):

    # Retrieve the study_id from the session
    selected_study_id = request.session.get('selected_study_id')
    with open('tasks/task_assignment.json', 'r') as assignment_file:
        study_assignment = json.load(assignment_file)

    with open('tasks/test_task.json', 'r') as assignment_file:
        test_task = json.load(assignment_file)

    # Get the task set associated with the study ID, defaulting to 'default_task_set' if not found
    task_set_name = study_assignment.get(selected_study_id, None)

    if not task_set_name:
        # assign task set at random
        task_set_name = random.choice(TASK_SETS)

    task_set = load_tasks(f'tasks/{task_set_name}.json')
    test_task = load_tasks(f'tasks/test_task.json')

    if task_number == 0:
        current_task = test_task

    elif task_number > NR_OF_TASKS:
        return redirect('duck_code_editor:break_page')

    else:
        current_task = task_set[task_number-1]

    output = None
    if request.method == 'POST':

        # new task is requested
        if 'next' in request.POST:
            # save time and solution in trial_task instance
            current_trial = Trial.objects.get(
                student_id=selected_study_id,
            )

            if task_number == 0:
                trial_task = current_trial.test_task

            elif task_number == 1:
                trial_task = current_trial.task_1

            elif task_number == 2:
                trial_task = current_trial.task_2

            elif task_number == 3:
                trial_task = current_trial.task_3

            trial_task.end_time = timezone.now()
            trial_task.duration = trial_task.end_time - trial_task.start_time
            trial_task.student_solution = request.POST.get('code')
            trial_task.save()

            return redirect('duck_code_editor:feedback', task_number=task_number)

        elif 'run_code' in request.POST:
            # If 'Run Code' button is pressed, execute the code
            form = CodeSnippetForm(request.POST)
            if form.is_valid():
                code_snippet = form.save()
                try:
                    output = '\n' + execute_code(code_snippet.code)
                except Exception as e:
                    output = f"Error: {e}"
            else:
                output = None

    else:
        if task_number == 0:
            # create Trial instance or get existing one
            if not Trial.objects.filter(student_id=selected_study_id).exists():
                Trial.objects.create(
                    student_id=selected_study_id,
                    group=task_set_name,
                )

        current_trial = Trial.objects.get(
            student_id=selected_study_id)

        def create_trial_task(title: str):
            current_task_instance = Trial_Task.objects.create(
                task_name=title,
                start_time=timezone.now(),
                solved_with_duck=False
            )

            return current_task_instance

        if task_number == 0:
            if not current_trial.test_task:
                current_trial_task = create_trial_task(current_task['title'])
                current_trial.test_task = current_trial_task

        elif task_number == 1:
            if not current_trial.task_1:
                current_trial_task = create_trial_task(current_task['title'])
                current_trial.task_1 = current_trial_task
        elif task_number == 2:
            if not current_trial.task_2:
                current_trial_task = create_trial_task(current_task['title'])
                current_trial.task_2 = current_trial_task
        elif task_number == 3:
            if not current_trial.task_3:
                current_trial_task = create_trial_task(current_task['title'])
                current_trial.task_3 = current_trial_task
        else:
            breakpoint()

        current_trial.save()

        form = CodeSnippetForm(
            initial={'code': current_task.get('code_to_debug', '')})

    return render(request, 'duck_code_editor/code_editor.html', {
        'form': form,
        'task_number': task_number,
        'output': output,
        'current_task': current_task,
        'duck': False,
    })


def code_editor_duck(request, task_number):
    # Retrieve the study_id from the session
    selected_study_id = request.session.get('selected_study_id')

    with open('tasks/task_assignment.json', 'r') as assignment_file:
        study_assignment = json.load(assignment_file)

    # Get the task set associated with the study ID, defaulting to 'default_task_set' if not found
    task_set_name = study_assignment.get(selected_study_id)

    # take the other task set than the one assigned via TASK_SETS
    if task_set_name == TASK_SETS[0]:
        task_set_name = TASK_SETS[1]
    else:
        task_set_name = TASK_SETS[0]

    task_set = load_tasks(f'tasks/{task_set_name}.json')

    if task_number > NR_OF_TASKS:
        return redirect('duck_code_editor:survey')

    else:
        current_task = task_set[task_number-1]

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
            if task_number == 1:
                trial_task = current_trial.task_1_duck

            elif task_number == 2:
                trial_task = current_trial.task_2_duck

            elif task_number == 3:
                trial_task = current_trial.task_3_duck

            trial_task.end_time = timezone.now()
            trial_task.duration = trial_task.end_time - trial_task.start_time
            trial_task.student_solution = request.POST.get('code')
            trial_task.save()

            return redirect('duck_code_editor:feedback_duck', task_number=task_number)

        elif 'run_code' in request.POST:
            # If 'Run Code' button is pressed, execute the code
            form = CodeSnippetForm(request.POST)
            if form.is_valid():
                code_snippet = form.save()
                try:
                    output = '\n' + execute_code(code_snippet.code)
                except Exception as e:
                    output = f"Error: {e}"
            else:
                output = None

    else:
        form = CodeSnippetForm(
            initial={'code': current_task.get('code_to_debug', '')})

        current_trial = Trial.objects.get(
            student_id=selected_study_id)

        def create_trial_task(title: str):
            current_task_instance = Trial_Task.objects.create(
                task_name=title,
                start_time=timezone.now(),
                solved_with_duck=True
            )
            return current_task_instance

        if task_number == 1:
            if not current_trial.task_1_duck:
                current_trial_task = create_trial_task(current_task['title'])
                current_trial.task_1_duck = current_trial_task
        elif task_number == 2:
            if not current_trial.task_2_duck:
                current_trial_task = create_trial_task(current_task['title'])
                current_trial.task_2_duck = current_trial_task
        elif task_number == 3:
            if not current_trial.task_3_duck:
                current_trial_task = create_trial_task(current_task['title'])
                current_trial.task_3_duck = current_trial_task
        else:
            breakpoint()

        current_trial.save()

    return render(request, 'duck_code_editor/code_editor.html', {
        'form': form,
        'task_number': task_number,
        'output': output,
        'current_task': current_task,
        'duck': True,
    })


def survey_complete(request):
    return render(request, 'duck_code_editor/survey_complete.html')


def execute_code(code):
    try:
        # Use subprocess to run the code in a separate process
        result = subprocess.run(
            ["python", "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10  # Set a timeout of 10 seconds
        )

        # Check if the process timed out
        if result.returncode == -signal.SIGTERM:
            return "Error: Execution timed out (> 10 seconds).\n Please refactor."

        # Check for subprocess execution errors
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        # Handle timeout (code takes more than 10s)
        return "Error: Code execution timed out (took more than 10 seconds). Please refactor your code."

    except Exception as e:
        # Handle other exceptions (e.g., runtime errors in the code)
        return f"Error: {str(e)}"


def load_tasks(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            tasks = json.load(file)
        return tasks
    except FileNotFoundError:
        return []  # Return an empty list if the file is not found or cannot be read
    except json.JSONDecodeError:
        return []  # Return an empty list if there's an issue decoding the JSON


def get_available_ids():
    # Assuming you have a fixed set of possible IDs (s1, s2, ..., s30)
    all_possible_ids = [f's{i}' for i in range(1, 31)]

    # Get a list of IDs that are already in use
    used_ids = Trial.objects.values_list('student_id', flat=True)

    # Filter out the used IDs from the possible IDs
    available_ids = [id for id in all_possible_ids if id not in used_ids]

    return available_ids


def generate_random_name():
    colors = [
        'Red', 'Blue', 'Green', 'Yellow', 'Purple',
        'Orange', 'Pink', 'Brown', 'Gray', 'Black',
        'White', 'Turquoise', 'Gold', 'Silver', 'Maroon',
        'Navy', 'Cyan', 'Magenta', 'Lime', 'Teal'
    ]
    animals = [
        'Dog', 'Cat', 'Elephant', 'Giraffe', 'Lion',
        'Monkey', 'Tiger', 'Zebra', 'Kangaroo', 'Penguin',
        'Panda', 'Koala', 'Hippopotamus', 'Gorilla', 'Polar Bear',
        'Snake', 'Cheetah', 'Ostrich', 'Dolphin', 'Kangaroo'
    ]
    while True:
        random_name = f"{random.choice(colors)}-{random.choice(animals)}"
        if not Trial.objects.filter(student_id=random_name).exists():
            return random_name


def start_experiment(request):
    available_ids = get_available_ids()

    if request.method == 'POST':
        if 'generate' in request.POST:
            random_name = generate_random_name()
            request.session['selected_study_id'] = random_name
            return render(request, 'duck_code_editor/start_experiment.html',
                          {'available_ids': available_ids,
                              'random_name': random_name}
                          )

        else:
            # Store the selected ID in the session
            if not request.session['selected_study_id']:
                selected_id = request.POST.get('study_id')
                request.session['selected_study_id'] = selected_id
            # Redirect to code_editor view without including study_id in the URL
            return redirect('duck_code_editor:instructions')
    else:
        request.session['selected_study_id'] = None

    # Render the start_experiment template
    return render(request, 'duck_code_editor/start_experiment.html', {'available_ids': available_ids})


def break_page(request):
    return render(request, 'duck_code_editor/break.html')


def instructions(request):
    if request.method == 'POST':
        return redirect('duck_code_editor:code_editor', task_number=0)
    return render(request, 'duck_code_editor/instructions.html')


def rubber_duck_instructions(request):
    if request.method == 'POST':
        if 'start-rubber-duck' in request.POST:
            return redirect('duck_code_editor:code_editor_duck', task_number=1)
        else:
            return render(request, 'duck_code_editor/rubber_duck_instructions.html')
    return render(request, 'duck_code_editor/rubber_duck_instructions.html')


def without_duck_instructions(request):
    if request.method == 'POST':
        if 'start-without-duck' in request.POST:
            return redirect('duck_code_editor:code_editor', task_number=1)
        else:
            return render(request, 'duck_code_editor/without_duck_instructions.html')
    return render(request, 'duck_code_editor/without_duck_instructions.html')


def feedback(request, task_number):
    selected_study_id = request.session.get('selected_study_id')
    current_trial = Trial.objects.get(student_id=selected_study_id)

    # depending on whether duck is in the URL as in task<nr>duck, redirect to the correct URL
    regex_pattern = re.compile(r'task\d+duck')
    duck_debugging = regex_pattern.search(request.path)
    if request.method == 'POST':
        if task_number == 0:
            current_trial_task = current_trial.test_task

        elif task_number == 1:
            current_trial_task = current_trial.task_1
            if duck_debugging:
                current_trial_task = current_trial.task_1_duck
        elif task_number == 2:
            current_trial_task = current_trial.task_2
            if duck_debugging:
                current_trial_task = current_trial.task_2_duck
        elif task_number == 3:
            current_trial_task = current_trial.task_3
            if duck_debugging:
                current_trial_task = current_trial.task_3_duck
        else:
            return HttpResponseBadRequest("Invalid task number")

        # Save the perceived complexity from the form submission
        perceived_complexity = request.POST.get('complexity')
        familiarity = request.POST.get('familiarity')
        talking = request.POST.get('talking')
        silence = request.POST.get('silence')

        if perceived_complexity:
            current_trial_task.perceived_complexity = perceived_complexity

        if familiarity:
            current_trial_task.familiarity = familiarity

        if talking:
            current_trial_task.talking = talking

        if silence:
            current_trial_task.silence = silence

        current_trial_task.save()

        if duck_debugging:
            return redirect('duck_code_editor:code_editor_duck', task_number=task_number+1)
        else:
            if task_number == 0:
                return redirect('duck_code_editor:without_instructions')
            else:
                return redirect('duck_code_editor:code_editor', task_number=task_number+1)

    return render(request, 'duck_code_editor/complexity_feedback.html', {
        'duck': duck_debugging,
        'test': task_number == 0,
    })


def survey(request):
    if request.method == 'POST':
        trial = Trial.objects.get(
            student_id=request.session.get('selected_study_id'))

        # Save survey responses to the database
        perception_q1 = request.POST.get('perception_q1')
        perception_q2 = request.POST.get('perception_q2')
        perception_q3 = request.POST.get('perception_q3')
        perception_q4 = request.POST.get('perception_q4')
        perception_q5 = request.POST.get('perception_q5')
        perception_q6 = request.POST.get('perception_q6')
        perception_q7 = request.POST.get('perception_q7')
        big_five_q1 = request.POST.get('big_five_q1')
        big_five_q2 = request.POST.get('big_five_q2')
        big_five_q3 = request.POST.get('big_five_q3')
        big_five_q4 = request.POST.get('big_five_q4')
        big_five_q5 = request.POST.get('big_five_q5')
        big_five_q6 = request.POST.get('big_five_q6')
        big_five_q7 = request.POST.get('big_five_q7')
        big_five_q8 = request.POST.get('big_five_q8')
        big_five_q9 = request.POST.get('big_five_q9')
        big_five_q10 = request.POST.get('big_five_q10')
        survey_q1 = request.POST.get('survey_q1')
        survey_q2 = request.POST.get('survey_q2')
        survey_q3 = request.POST.get('survey_q3')

        # Save to your model instance (replace YourModel with the actual name of your model)
        trial.survey_q1 = survey_q1
        trial.survey_q2 = survey_q2
        trial.survey_q3 = survey_q3
        trial.perception_q1 = perception_q1
        trial.perception_q2 = perception_q2
        trial.perception_q3 = perception_q3
        trial.perception_q4 = perception_q4
        trial.perception_q5 = perception_q5
        trial.perception_q6 = perception_q6
        trial.perception_q7 = perception_q7
        trial.big_five_q1 = big_five_q1
        trial.big_five_q2 = big_five_q2
        trial.big_five_q3 = big_five_q3
        trial.big_five_q4 = big_five_q4
        trial.big_five_q5 = big_five_q5
        trial.big_five_q6 = big_five_q6
        trial.big_five_q7 = big_five_q7
        trial.big_five_q8 = big_five_q8
        trial.big_five_q9 = big_five_q9
        trial.big_five_q10 = big_five_q10

        trial.save()

        return redirect('duck_code_editor:survey_complete')

    return render(request, 'duck_code_editor/survey.html')
