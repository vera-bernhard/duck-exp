# Generated by Django 4.2.7 on 2023-11-20 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("duck_code_editor", "0002_remove_codesnippet_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("code_to_debug", models.TextField()),
                ("expected_output", models.TextField()),
                ("complexity", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Trial_Task",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("task_name", models.CharField(max_length=50)),
                ("student_solution", models.TextField()),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("duration", models.DurationField()),
                ("solved_with_duck", models.BooleanField()),
                ("perceived_complexity", models.CharField(max_length=50)),
                ("trial_position", models.CharField(max_length=50)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="duck_code_editor.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Trial",
            fields=[
                (
                    "student_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("group", models.CharField(max_length=50)),
                ("survey_q1", models.CharField(max_length=50)),
                ("survey_q2", models.CharField(max_length=50)),
                ("survey_q3", models.CharField(max_length=50)),
                (
                    "task_1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_1",
                        to="duck_code_editor.trial_task",
                    ),
                ),
                (
                    "task_1_duck",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_1_duck",
                        to="duck_code_editor.trial_task",
                    ),
                ),
                (
                    "task_2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_2",
                        to="duck_code_editor.trial_task",
                    ),
                ),
                (
                    "task_2_duck",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_2_duck",
                        to="duck_code_editor.trial_task",
                    ),
                ),
                (
                    "test_task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test_task",
                        to="duck_code_editor.trial_task",
                    ),
                ),
            ],
        ),
    ]
