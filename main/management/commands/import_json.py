import json
import os
from main.models import Experiment, Sample, Sample_Metadata, Read_Pair  
from django.core.management.base import BaseCommand
from datetime import datetime 


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        #################################################
        # Part 1: Load JSON and find correct file paths #
        #################################################

        # Determine the correct path to the JSON file
        base_dir = os.path.dirname(os.path.abspath(__file__)) # was having trouble with the path to the json file so I used this instead of a direct path
        json_file_path = os.path.join(base_dir, 'cleaned_migration.json')

        # Load JSON data from file
        with open(json_file_path, 'r') as file:  
            data = json.load(file)

        for item in data:

        ####################################
        # Part 2: Handle Experiments Model #
        ####################################

            '''The experiments are saved as acronyms, but I want the full exp name to be
            saved to the db. The next few lines corelate the acronym to the exp name so that can be 
            saved to the db instead'''

            experiment_id = item.get('Experiment ID')  
            exp_names = {'SI': "Stable Infection", 'RMF': "Riv84 Merill23", 'MW': 'Mixed wMel-wWil'} 

            # Check if the experiment ID exists in the dictionary and get the full name
            if experiment_id in exp_names:
                experiment_name = exp_names[experiment_id]
            else:
                experiment_name = experiment_id  # Fallback if initials not found

            #create exp
            experiment, created = Experiment.objects.get_or_create(name=experiment_name) 
            if created: #bool = true if exp *didnt* exist before
                self.stdout.write(f"Created New Experiment: {experiment.name}")

        ################################
        # Part 3: Handle Samples Model #
        ################################

            #Part 3A: Sample ID and Label
            sample_id = item.get('Sample ID')    
            sample_label = item.get('Sample Label')  

            #Part 3B: Date validation
            created_date = item.get('Date Collected')

             # Check if 'Date Collected' exists and is in a valid format
            if created_date:
                try:
                    datetime.strptime(created_date, '%Y-%m-%d')  # Just to validate the format
                except ValueError:
                    # Throw an error if the date format is incorrect
                    self.stdout.write(self.style.ERROR(f"Invalid date format for sample '{sample_id}': {created_date}"))
            else:
                # throw an error if 'Date Collected' is missing
                self.stdout.write(self.style.ERROR(f"Missing 'Date Collected' for sample '{sample_id}'"))

            #Part 3C: DB Commit
            sample, created = Sample.objects.update_or_create(
                sample_id=sample_id,
                defaults={
                    'created_date': created_date,
                    'experiment': experiment,
                    'sample_label': sample_label
                })
            # Check if a new sample was created
            if created:
                print(f"Created New Sample: {sample.sample_id}")
            else:
                print(f"Updated Sample: {sample.sample_id}")

        #################################
        # Part 4: Handle Metadata Model #
        #################################

            metadata = {
                "Cell_Line": item.get('Cell Line'),
                "Infection": item.get('Infection'),
                "Initials": item.get('Initials'),
                "Split (DDMMRep)": item.get('Split (DDMMRep)'),
                "Species":item.get('Species'),
                'Replicate':item.get('Pellet Replicate'),
                "Extraction Date":item.get('Extraction Date'),
                "Timepoint":item.get('Timepoint'),
                'gDNA Conc':item.get('gDNA Conc'),
                'media':item.get('Media Type'),
            }  

            # Update or create metadata
            sample_metadata, created = Sample_Metadata.objects.update_or_create(
                sample_id=sample,
                defaults={'metadata': metadata})

            if created:
                self.stdout.write(f"Created New Metadata for Sample: {sample.sample_id}")
            else:
                self.stdout.write(f"Updated Metadata for Sample: {sample.sample_id}")


        ##################################
        # Part 5: Handle Read Pair Model #
        ##################################

            read1_path = f"/path/to/read1_{sample_id}.fastq" 
            read2_path = f"/path/to/read2_{sample_id}.fastq"  
            plate_number = item.get('Plate Number', '0') # Default to '0' if Plate Number is not found

            # Create or update Read Pair Path
            read_pair, created = Read_Pair.objects.update_or_create(
                read1_path=read1_path,
                sample_id=sample,
                defaults={
                    'read2_path': read2_path,
                    'plate_number': plate_number
                })
            
            if created:
                self.stdout.write(f"Created New Read Pair for Sample: {sample.sample_id}")
