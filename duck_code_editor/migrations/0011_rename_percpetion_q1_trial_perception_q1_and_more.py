# Generated by Django 4.2.7 on 2023-11-27 22:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("duck_code_editor", "0010_trial_big_five_q1_trial_big_five_q10_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="trial",
            old_name="percpetion_q1",
            new_name="perception_q1",
        ),
        migrations.RenameField(
            model_name="trial",
            old_name="percpetion_q2",
            new_name="perception_q2",
        ),
        migrations.RenameField(
            model_name="trial",
            old_name="percpetion_q3",
            new_name="perception_q3",
        ),
        migrations.RenameField(
            model_name="trial",
            old_name="percpetion_q4",
            new_name="perception_q4",
        ),
        migrations.RenameField(
            model_name="trial",
            old_name="percpetion_q5",
            new_name="perception_q5",
        ),
        migrations.RenameField(
            model_name="trial",
            old_name="percpetion_q6",
            new_name="perception_q6",
        ),
        migrations.RenameField(
            model_name="trial",
            old_name="percpetion_q7",
            new_name="perception_q7",
        ),
    ]