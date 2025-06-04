import os
import csv
import json


def get_ohdsi_data(dir:str)->list:
    ohdsi = []
    for csv_file in os.listdir(dir):
        file_path = os.path.join(dir,csv_file)
        with open(file_path,'r') as file:
            dictreader = csv.DictReader(file)

            for row in dictreader:
                row['Cohort_id'] = int(csv_file.split("-")[0].strip("C"))
                ohdsi.append(row)
    return ohdsi

def get_detail(dir:str)->list:
    with open(dir,'r') as file:
        file = file.read()
        ohdsi_detail = json.loads(file)
    return ohdsi_detail

def get_concept(ohdsi:list,detail:list)->list:
    ohdsi_concept = []
    concept_id_list = []
    i = 0
    for row in ohdsi:
        i += 1
        print(f"{i}")
        if row['Concept Id'] not in concept_id_list:
            concept_id_list.append(row['Concept Id'])
            detail_dictionary = {}
            detail_dictionary['Concept_ID'] = int(row.get('Concept Id','NA'))
            detail_dictionary['Concept_Name'] = row.get('Concept Name','NA')
            detail_dictionary['Vocabulary_ID'] = [row.get('Vocabulary Id','NA')]
            detail_dictionary['Concept_code'] = [row.get('Concept Code','NA')]
            detail_dictionary['Cohort_ID'] = [item['Cohort_id'] for item in detail if item['Cohort_id'] == row['Cohort_id']]
            detail_dictionary['Cohort_name'] = [item['Cohort_name'] for item in detail if item['Cohort_id'] == row['Cohort_id']]
            detail_dictionary['PIDs'] = [item['PID'] for item in detail if item['Cohort_id'] == row['Cohort_id']]
            ohdsi_concept.append(detail_dictionary)
        else:
            for concept in ohdsi_concept:
                if concept['Concept_ID'] == int(row['Concept Id']):
                    concept['Vocabulary_ID'].append(row.get('Vocabulary Id','NA'))
                    concept['Concept_code'].append(row.get('Concept Code','NA'))
                    concept['Cohort_ID'].extend([item['Cohort_id'] for item in detail if item['Cohort_id'] == row['Cohort_id']])
                    concept['Cohort_name'].extend([item['Cohort_name'] for item in detail if item['Cohort_id'] == row['Cohort_id']])
                    concept['PIDs'].extend([item['PID'] for item in detail if item['Cohort_id'] == row['Cohort_id']])

    sorted_concept = sorted(ohdsi_concept,key = lambda x: x['Concept_ID']) 
    i = 0
    for concept in sorted_concept:
        i += 1
        concept['CID'] = f'OC{i:06d}'

    return sorted_concept
