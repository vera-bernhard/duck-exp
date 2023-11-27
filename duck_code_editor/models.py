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
    test_task = models.ForeignKey('Trial_Task', related_name='test_task', on_delete=models.CASCADE, null=True, default=None)
    task_1 = models.ForeignKey('Trial_Task', related_name='task_1', on_delete=models.CASCADE, null=True, default=None)
    task_2 = models.ForeignKey('Trial_Task', related_name='task_2', on_delete=models.CASCADE, null=True, default=None)
    task_3 = models.ForeignKey('Trial_Task', related_name='task_3', on_delete=models.CASCADE, null=True, default=None)
    task_1_duck = models.ForeignKey('Trial_Task', related_name='task_1_duck', on_delete=models.CASCADE, null=True, default=None)
    task_2_duck = models.ForeignKey('Trial_Task', related_name='task_2_duck', on_delete=models.CASCADE, null=True, default=None)
    task_3_duck = models.ForeignKey('Trial_Task', related_name='task_3_duck', on_delete=models.CASCADE, null=True, default=None)
    survey_q1 = models.CharField(max_length=50, null=True, default=None)
    survey_q2 = models.CharField(max_length=50, null=True, default=None)
    survey_q3 = models.CharField(max_length=50, null=True, default=None)
    perception_q1 = models.CharField(max_length=50, null=True, default=None)
    perception_q2 = models.CharField(max_length=50, null=True, default=None)
    perception_q3 = models.CharField(max_length=50, null=True, default=None)
    perception_q4 = models.CharField(max_length=50, null=True, default=None)
    perception_q5 = models.CharField(max_length=50, null=True, default=None)
    perception_q6 = models.CharField(max_length=50, null=True, default=None)
    perception_q7 = models.CharField(max_length=50, null=True, default=None)
    big_five_q1 = models.CharField(max_length=50, null=True, default=None)
    big_five_q2 = models.CharField(max_length=50, null=True, default=None)
    big_five_q3 = models.CharField(max_length=50, null=True, default=None)
    big_five_q4 = models.CharField(max_length=50, null=True, default=None)
    big_five_q5 = models.CharField(max_length=50, null=True, default=None)
    big_five_q6 = models.CharField(max_length=50, null=True, default=None)
    big_five_q7 = models.CharField(max_length=50, null=True, default=None)
    big_five_q8 = models.CharField(max_length=50, null=True, default=None)
    big_five_q9 = models.CharField(max_length=50, null=True, default=None)
    big_five_q10 = models.CharField(max_length=50, null=True, default=None)

class Trial_Task(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=50)
    student_solution = models.TextField(default='')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(default=None, null=True)
    duration = models.DurationField(default=None, null=True)
    solved_with_duck = models.BooleanField()
    perceived_complexity = models.CharField(max_length=50, null=True)
    familiarity = models.CharField(max_length=50, null=True)
    talking = models.CharField(max_length=50, null=True)
    silence = models.CharField(max_length=50, null=True)

    # Foreign key to the Task model to link the specific task details
    # task = models.ForeignKey(Task, on_delete=models.CASCADE)
