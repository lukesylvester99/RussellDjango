import os
from dotenv import  load_dotenv, dotenv_values
import gspread
from google.oauth2.service_account import Credentials
import json

load_dotenv()

# Construct the service account information from environment variables
service_account_info = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'), 
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
}

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

#accessing pellet and tn5 sheets with client credentials
sheet_id_pellets = '12Cy2HZpVzzzu_erg2XMXCAd19XY88hfhDKUOA5MIDGs' #replace with real id once testing is done!!
sheet_id_tn5 = '13VX6wxF4RHhlJwSEei8kdpTNyGBrq3sgOliiDDZWDsc'
pellet_sheet = client.open_by_key(sheet_id_pellets)
tn5_sheet = client.open_by_key(sheet_id_tn5)

#saving these 'accessed' sheets in an obj that I can call alter
values_list_pellets = pellet_sheet.worksheets() 
values_list_tn5= tn5_sheet.worksheets()

names = []
for worksheet in values_list_pellets: #iterating through pellet samples sheet and saving tab names
    name = worksheet.title
    if name not in ["Instructions", "Experiment Template", "Experiments Summary", "Needs Extraction"]:
        names.append(name)

json_data = [] #this will get saved as a json file later
for name in names: #saving all sheet information for each exp tab in sheet
    worksheet = pellet_sheet.worksheet(name)
    all_records = worksheet.get_all_records()


    # Filter out rows where Column E ('Date Collected') is empty
    filtered_records = [row for row in all_records if row.get('Date Collected')] 

    json_data.extend(filtered_records) 

#I need to connect tn5 sheet so that I can get plate data and gDNA concentrations
tn5_worksheet = tn5_sheet.worksheet('gDNA concentrations')
all_records_tn5 = tn5_worksheet.get_all_records()
for record in all_records_tn5:
    for i in json_data:
        sample_id = record.get('Sample') #get sample name from sheet

        # Match by "Sample ID" or "Sample Label"
        if sample_id == i.get("Sample ID") or sample_id == i.get("Sample Label") or sample_id == i.get("Original Sample Name"):
            i["gDNA Conc"] = record.get('gDNA Concentration (ng/ul)', '')  #save to json obj

            plate_number = record.get('Plate #')
            if plate_number != 'NA':# Skip if Plate Number is 'NA'                
                i["Plate Number"] = plate_number

# Directory where json file will be saved.
output_dir = r'C:\Users\lukes\OneDrive\Documents\GitHub\titerDjango\titerpipeline\main\management\commands'
output_file = os.path.join(output_dir, 'cleaned_migration.json')

with open(output_file, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"JSON data successfully saved to {output_file}")