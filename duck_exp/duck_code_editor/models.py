from django.db import models

class CodeSnippet(models.Model):
    code = models.TextField()

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    code_to_debug = models.TextField()
    expected_output = models.TextField()
    complexity = models.CharField(max_length=50)

class Trial(models.Model):
    student_id = models.CharField(max_length=50, primary_key=True)
    group = models.CharField(max_length=50)
    test_task = models.ForeignKey('Trial_Task', related_name='test_task', on_delete=models.CASCADE)
    task_1 = models.ForeignKey('Trial_Task', related_name='task_1', on_delete=models.CASCADE)
    task_2 = models.ForeignKey('Trial_Task', related_name='task_2', on_delete=models.CASCADE)
    task_1_duck = models.ForeignKey('Trial_Task', related_name='task_1_duck', on_delete=models.CASCADE)
    task_2_duck = models.ForeignKey('Trial_Task', related_name='task_1_duck', on_delete=models.CASCADE)
    survey_q1 = models.CharField(max_length=50)
    survey_q2 = models.CharField(max_length=50)
    survey_q3 = models.CharField(max_length=50)


class Trial_Task(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=50)
    student_solution = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    solved_with_duck = models.BooleanField()
    perceived_complexity = models.CharField()

    # Foreign key to the Task model to link the specific task details
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
