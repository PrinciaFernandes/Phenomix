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
        if phenotype['Overview']['Outcome'] not in outcome_list:
            outcome_list.append(phenotype['Overview']['Outcome'])        
            detail_dictionary = {}
            detail_dictionary['Outcome'] = phenotype['Overview']['Outcome']
            detail_dictionary['Title'] = phenotype['Overview']['Title']
            detail_dictionary['Request_id'] = phenotype['Overview']['Request IDs'] if phenotype['Overview']['Request IDs'] else 'NA'
            detail_dictionary['Query_start_date'],detail_dictionary['Query_end_date'] = get_query_date(phenotype['Overview']['Query period'])
            detail_dictionary['Description'] = phenotype['Overview']['Description']
            detail_dictionary['Algorithm_to_define_outcome'] = phenotype['Overview']['Algorithm to define outcome']
            detail_dictionary['Request_send_date'] = get_request_date(phenotype['Overview']['Request to send dates'])
            sentinel_detail.append(detail_dictionary)
        else:
            for detail in sentinel_detail:
                if detail['Outcome'] == phenotype['Overview']['Outcome']:
                    detail['Title'] = detail['Title']+ f' \n {phenotype['Overview']['Title']}' 
                    detail['Request_id'] = detail['Request_id']+ f' \n {phenotype['Overview']['Request IDs']}' 
                    query_start_date,query_end_date = get_query_date(phenotype['Overview']['Request to send dates'])
                    detail['Query_start_date'] = detail['Query_start_date']+ f' \n {query_start_date}'
                    detail['Query_end_date'] = detail['Query_end_date']+ f' \n {query_end_date}' 
                    detail['Description'] = detail['Description']+ f' \n {phenotype['Overview']['Description']}' 
                    detail['Algorithm_to_define_outcome'] = detail['Algorithm_to_define_outcome']+ f' \n {phenotype['Overview']['Algorithm to define outcome']}' 
                    detail['Request_send_date'] = detail['Request_send_date']+ f' \n {get_request_date(phenotype['Overview']['Request to send dates'])}' 
        
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
                concept_dictioanry['Code'] =  codes['Code']
                concept_dictioanry['Description'] = codes['Description'] if codes['Description'] else ['NA']
                concept_dictioanry['Care_setting'] = [codes['Care_setting']] if 'Care_setting' in codes.keys() else ['NA']
                concept_dictioanry['Code_type']= [codes['Code_Type']] if 'Code_Type' in codes.keys() else ['NA']
                concept_dictioanry['Code_category']= [codes['Code_Category']] if 'Code_Category' in codes.keys() else ['NA']
                concept_dictioanry['Principal_diagnosis']= [codes['Principal diagnosis']] if 'Principal_diagnosis' in codes.keys() else ['NA']
                concept_dictioanry['Outcome']= [phenotype['Overview']['Outcome']]
                concept_dictioanry['Request_id']= [phenotype['Overview']['Request IDs']]
                concept_dictioanry['PIDs']= [d['PID'] for d in detail if d['Outcome'] == phenotype['Overview']['Outcome']]
                sentinel_concept.append(concept_dictioanry)
            else:
                for concept in sentinel_concept:
                    if concept['Code'] == codes['Code']:
                        concept['Care_setting'].append(codes['Care_setting']) if 'Care_setting' in codes.keys() else concept['Care_setting'].append('NA')
                        concept['Code_type'].append(codes['Code_Type']) if 'Code_Type' in codes.keys() else concept['Code_type'].append('NA')
                        concept['Code_category'].append(codes['Code_Category']) if 'Code_Category' in codes.keys() else concept['Code_category'].append('NA')
                        concept['Principal_diagnosis'].append(codes['Principal_diagnosis']) if 'Principal_diagnosis' in codes.keys() else concept['Principal_diagnosis'].append('NA')
                        concept['Outcome'].append(phenotype['Overview']['Outcome'])
                        concept['Request_id'].append(phenotype['Overview']['Request IDs']) if phenotype['Overview']['Request IDs'] else concept['Request_id'].append('NA')
                        concept['PIDs'].extend([d['PID'] for d in detail if d['Outcome'] == phenotype['Overview']['Outcome']])

    sorted_concept = sorted(sentinel_concept,key = lambda x: x['Code'])
    i = 0
    for dict in sorted_concept:
        i += 1
        dict['CID'] = f'SC{i:06d}'

    return sorted_concept
