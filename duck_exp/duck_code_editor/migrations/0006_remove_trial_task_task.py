# Generated by Django 4.2.7 on 2023-11-20 12:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "duck_code_editor",
            "0005_alter_trial_task_duration_alter_trial_task_end_time",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trial_task",
            name="task",
        ),
    ]
