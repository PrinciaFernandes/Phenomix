import os
import csv
import json


def get_ohdsi_data(dir):
    ohdsi = []
    for csv_file in os.listdir(dir):
        file_path = os.path.join(dir,csv_file)
        with open(file_path,'r') as file:
            dictreader = csv.DictReader(file)

            for row in dictreader:
                row['Cohort_id'] = int(csv_file.split("-")[0].strip("C"))
                ohdsi.append(row)
    return ohdsi

def get_detail(dir):
    with open(dir,'r') as file:
        file = file.read()
        ohdsi_detail = json.loads(file)
    return ohdsi_detail

def get_concept(ohdsi,detail):
    ohdsi_concept = []
    concept_id_list = []
    i = 0
    for row in ohdsi:
        i += 1
        print(f"{i}")
        if row['Concept Id'] not in concept_id_list:
            concept_id_list.append(row['Concept Id'])
            detail_dictionary = {}
            detail_dictionary['Concept_ID'] = int(row['Concept Id'])
            detail_dictionary['Concet_Name'] = row['Concept Name']
            detail_dictionary['Vocabulary_ID'] = [row['Vocabulary Id'] if row['Vocabulary Id'] else 'NA']
            detail_dictionary['Concept_code'] = [row['Concept Code'] if row['Concept Code'] else 'NA']
            detail_dictionary['Cohort_ID'] = [r['Cohort_id'] for r in detail if r['Cohort_id'] == row['Cohort_id']]
            detail_dictionary['Cohort_name'] = [d['Cohort_name'] for d in detail if d['Cohort_id'] == row['Cohort_id']]
            detail_dictionary['PIDs'] = [d['PID'] for d in detail if d['Cohort_id'] == row['Cohort_id']]
            ohdsi_concept.append(detail_dictionary)
        else:
            for concept in ohdsi_concept:
                if concept['Concept_ID'] == int(row['Concept Id']):
                    concept['Vocabulary_ID'].append(row['Vocabulary Id'] if row['Vocabulary Id'] else 'NA')
                    concept['Concept_code'].append(row['Concept Code'] if row['Concept Code'] else 'NA')
                    concept['Cohort_ID'].extend([r['Cohort_id'] for r in detail if r['Cohort_id'] == row['Cohort_id']])
                    concept['Cohort_name'].extend([d['Cohort_name'] for d in detail if d['Cohort_id'] == row['Cohort_id']])
                    concept['PIDs'].extend([d['PID'] for d in detail if d['Cohort_id'] == row['Cohort_id']])
    
    sorted_concept = sorted(ohdsi_concept,key = lambda x: x['Concept_ID']) 
    i = 0
    for concept in sorted_concept:
        i += 1
        concept['CID'] = f'OC{i:06d}'

    return sorted_concept
