from datetime import datetime
import re

def get_query_date(date):
    if date:
        query_period = date.replace(" to "," - ")
        query_period = date.replace(" – "," - ")

        query_dates = re.findall(r"\b[A-Za-z]+\s\d{1,2},\s\d{4}\s-\s[A-Za-z]+\s\d{1,2},\s\d{4}|\b\d{4}\s*-\s*\d{4}\b",query_period)
        if any(" - " in d for d in query_dates): 
            start_date = [datetime.strptime(date.split(" - ")[0],"%B %d, %Y") for date in query_dates]
            end_date = [datetime.strptime(date.split(" - ")[-1],"%B %d, %Y") for date in query_dates]
        else:
            start_date = [datetime.strptime(date.split("-")[0],"%Y") for date in query_dates]
            end_date = [datetime.strptime(date.split("-")[-1],"%Y") for date in query_dates]
        Query_start_date = ", ".join([datetime.strftime(date,"%Y-%m-%dT%H:%M:%S.00Z") for date in start_date])
        Query_end_date = ", ".join([datetime.strftime(date,"%Y-%m-%dT%H:%M:%S.00Z") for date in end_date])
    else:
        Query_start_date = 'NA'
        Query_end_date = 'NA'
    return Query_start_date,Query_end_date

def get_request_date(date):
    if date:
        request_date = re.findall(r"\b[A-Za-z]+\s\d{1,2},\s\d{4}",date)
        Request_date = [datetime.strptime(date,"%B %d, %Y") for date in request_date]
        Request_send_date = ", ".join([datetime.strftime(date,"%Y-%m-%dT%H:%M:%S.00Z") for date in Request_date])
    else:
        Request_send_date = 'NA'
    return Request_send_date

def get_detail(sentinel):
    outcome_list = []
    sentinel_detail = []

    for phenotype in sentinel:
        phenotype_overview = phenotype['Overview']
        if phenotype_overview['Outcome'] not in outcome_list:
            outcome_list.append(phenotype_overview['Outcome'])        
            detail_dictionary = {}
            detail_dictionary['Outcome'] = phenotype_overview.get('Outcome', 'NA')
            detail_dictionary['Title'] = phenotype_overview.get('Title', 'NA')
            detail_dictionary['Request_id'] = phenotype_overview.get('Request IDs', 'NA')
            detail_dictionary['Query_start_date'],detail_dictionary['Query_end_date'] = get_query_date(phenotype_overview.get('Query period', 'NA'))
            detail_dictionary['Description'] = phenotype_overview.get('Description', 'NA')
            detail_dictionary['Algorithm_to_define_outcome'] = phenotype_overview.get('Algorithm to define outcome', 'NA')
            detail_dictionary['Request_send_date'] = get_request_date(phenotype_overview.get('Request to send dates', 'NA'))
            sentinel_detail.append(detail_dictionary)
        else:
            for detail in sentinel_detail:
                if detail['Outcome'] == phenotype_overview['Outcome']:
                    detail['Title'] = detail['Title']+ f' \n {phenotype_overview.get('Title', 'NA')}'
                    detail['Request_id'] = detail['Request_id']+ f' \n {phenotype_overview.get('Request IDs', 'NA')}'
                    query_start_date,query_end_date = get_query_date(phenotype_overview.get('Request to send dates', 'NA'))
                    detail['Query_start_date'] = detail['Query_start_date']+ f' \n {query_start_date}'
                    detail['Query_end_date'] = detail['Query_end_date']+ f' \n {query_end_date}' 
                    detail['Description'] = detail['Description']+ f' \n {phenotype_overview.get('Description', 'NA')}' 
                    detail['Algorithm_to_define_outcome'] = detail['Algorithm_to_define_outcome']+ f' \n {phenotype_overview.get('Algorithm to define outcome', 'NA')}' 
                    detail['Request_send_date'] = detail['Request_send_date']+ f' \n {get_request_date(phenotype_overview.get('Request to send dates', 'NA'))}' 

    sorted_detail = sorted(sentinel_detail,key = lambda x: x['Outcome'])

    i = 0
    for detail in sorted_detail:
        i += 1
        detail['PID'] = f'SP{i:06d}'

    return sorted_detail

def get_concept(sentinel,detail):
    sentinel_concept = []
    code_list = []
    for phenotype in sentinel:
        for codes in phenotype['Code_Description']: 
            if codes['Code'] not in code_list:
                code_list.append(codes['Code'])
                concept_dictioanry = {}
                concept_dictioanry['Code'] =  codes.get('Code', 'NA')
                concept_dictioanry['Description'] = codes.get('Description', 'NA')
                concept_dictioanry['Care_setting'] = [codes.get('Care_setting', 'NA')]
                concept_dictioanry['Code_type']= [codes.get('Code_Type', 'NA')]
                concept_dictioanry['Code_category']= [codes.get('Code_Category', 'NA')]
                concept_dictioanry['Principal_diagnosis']= [codes.get('Principal diagnosis', 'NA')]
                concept_dictioanry['Outcome']= [phenotype['Overview'].get('Outcome', 'NA')]
                concept_dictioanry['Request_id']= [phenotype['Overview'].get('Request IDs', 'NA')]
                concept_dictioanry['PIDs']= [item['PID'] for item in detail if item['Outcome'] == phenotype['Overview'].get('Outcome', 'NA')]
                sentinel_concept.append(concept_dictioanry)
            else:
                for concept in sentinel_concept:
                    if concept['Code'] == codes['Code']:
                        concept['Care_setting'].append(codes.get('Care_setting', 'NA'))
                        concept['Code_type'].append(codes.get('Code_Type', 'NA'))
                        concept['Code_category'].append(codes.get('Code_Category', 'NA'))
                        concept['Principal_diagnosis'].append(codes.get('Principal_diagnosis', 'NA'))
                        concept['Outcome'].append(phenotype['Overview'].get('Outcome', 'NA'))
                        concept['Request_id'].append(phenotype['Overview'].get('Request IDs', 'NA'))
                        concept['PIDs'].extend([item['PID'] for item in detail if item['Outcome'] == phenotype['Overview'].get('Outcome', 'NA')])

    sorted_concept = sorted(sentinel_concept,key = lambda x: x['Code'])
    i = 0
    for dict in sorted_concept:
        i += 1
        dict['CID'] = f'SC{i:06d}'

    return sorted_concept
