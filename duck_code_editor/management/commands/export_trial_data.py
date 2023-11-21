# yourapp/management/commands/export_trial_data.py
import csv
from django.core.management.base import BaseCommand
from duck_code_editor.models import Trial, Trial_Task

class Command(BaseCommand):
    help = 'Export data from Trial and Trial_Task models to CSV files'

    def handle(self, *args, **options):
        # Specify the path to the CSV files
        trial_output_file = 'trial_data.csv'
        trial_task_output_file = 'trial_task_data.csv'

        # Get the data from the Trial model
        trial_data = Trial.objects.all()

        # Write the Trial data to the CSV file
        with open(trial_output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
           
            # Write the header row
            header = [field.name for field in Trial._meta.fields]
            csv_writer.writerow(header)

            # Write the data rows
            for row in trial_data:
                # Enclose CharField values in quotes
                row_data = [f'"{getattr(row, field)}"' if isinstance(getattr(row, field), str) else getattr(row, field) for field in header]
                csv_writer.writerow(row_data)

        self.stdout.write(self.style.SUCCESS(f'Trial data exported to {trial_output_file}'))

        # Get the data from the Trial_Task model
        trial_task_data = Trial_Task.objects.all()

        # Write the Trial_Task data to the CSV file
        with open(trial_task_output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
           
            # Write the header row
            header = [field.name for field in Trial_Task._meta.fields]
            csv_writer.writerow(header)

            # Write the data rows
            for row in trial_task_data:
                # Enclose CharField values in quotes
                row_data = [f'"{getattr(row, field)}"' if isinstance(getattr(row, field), str) else getattr(row, field) for field in header]
                csv_writer.writerow(row_data)

        self.stdout.write(self.style.SUCCESS(f'Trial_Task data exported to {trial_task_output_file}'))
