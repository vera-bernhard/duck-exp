# Generated by Django 4.2.7 on 2023-11-20 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("duck_code_editor", "0003_task_trial_task_trial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trial_task",
            name="trial_position",
        ),
        migrations.AlterField(
            model_name="trial_task",
            name="duration",
            field=models.DurationField(default=None),
        ),
        migrations.AlterField(
            model_name="trial_task",
            name="end_time",
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name="trial_task",
            name="perceived_complexity",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="trial_task",
            name="student_solution",
            field=models.TextField(default=""),
        ),
    ]
