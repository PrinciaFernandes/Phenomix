from datetime import datetime
import re


def date_extract(date):
    if date == "" or date is None:
        event_start_date = "NA"
        event_end_date = "NA"
    else:
        date1 = date.replace(' - ','-').replace(' to ','-').replace(' and ','-')
        date2 = date1.replace('Start', "NA").replace('start', "NA")
        
        if not re.match(r'\d{4}-\d{4}',date2):
            Start_date = date2.split("-")[0]
            End_date = date2.split("-")[-1]

            if Start_date != 'NA':
                try:
                    start_date = datetime.strptime(Start_date,"%Y/%m/%d") if re.match(r'^\d{4}',Start_date) else datetime.strptime(Start_date,"%d/%m/%Y")
                    event_start_date = datetime.strftime(start_date,"%Y-%m-%dT%H:%M:%S.00Z")
                except:
                    event_start_date = 'Invalid date'
            else:
                event_start_date = 'NA'

            if End_date != 'NA':
                try:
                    end_date = datetime.strptime(End_date,"%Y/%m/%d") if re.match(r'^\d{4}',End_date) else datetime.strptime(End_date,"%d/%m/%Y")
                    event_end_date = datetime.strftime(end_date,"%Y-%m-%dT%H:%M:%S.00Z")
                except:
                    event_end_date = 'Invalid date'  
            else:
                event_end_date = 'NA'

        else:

            Start_date = date2.split("-")[0]
            End_date = date2.split("-")[-1]

            start_date = datetime.strptime(Start_date,"%Y") 
            end_date = datetime.strptime(End_date,"%Y")     
            event_start_date = datetime.strftime(start_date,"%Y-%m-%dT%H:%M:%S.00Z")
            event_end_date = datetime.strftime(end_date,"%Y-%m-%dT%H:%M:%S.00Z")
        
    return event_start_date,event_end_date

def get_detail(hdruk):
    hdruk_detail = []

    for data in hdruk:
        detail_dictionary = {}
        detail = data['details'][0]
        detail_dictionary["Phenotype_id"] = detail['phenotype_id'] if detail['phenotype_id'] else 'NA'
        detail_dictionary["Phenotype_version_id"] = int(detail['phenotype_version_id']) if detail['phenotype_version_id'] else 'NA'
        detail_dictionary["Name"] = detail['name'] if detail['name'] else 'NA'
        detail_dictionary["Defination"] = detail['definition'] if detail['definition'] else 'NA'
        detail_dictionary["Implementation"] = detail['implementation'] if detail['implementation'] else 'NA'
        detail_dictionary["Publications"] = detail['publications'] if detail['publications'] else 'NA'
        detail_dictionary["Validation"] = detail["validation"] if detail["validation"] else 'NA'
        detail_dictionary["Citation_requirements"] = detail["citation_requirements"] if detail["citation_requirements"] else 'NA'
        detail_dictionary["Created"] = detail["created"] if detail["created"] else 'NA'
        detail_dictionary["author"] = detail["author"] if detail["author"] else 'NA'
        detail_dictionary["Collections"] = [name ['name'] for name in detail['collections']] if detail['collections'] else 'NA'
        detail_dictionary["Tags"] = detail["tags"] if detail["tags"] else 'NA'
        detail_dictionary["Group"] = detail["group"] if detail["group"] else 'NA'
        detail_dictionary["Group_access"] = int(detail["group_access"]) if detail["group_access"] else 'NA'
        detail_dictionary["World_access"] = int(detail["world_access"]) if detail["world_access"] else 'NA'
        detail_dictionary["Updated"] = detail["updated"] if detail["updated"] else 'NA'
        detail_dictionary["Sex"] = detail['sex'][0]["name"] if detail['sex'] else 'NA'
        detail_dictionary["Type"] = detail['type'][0]["name"] if detail['type'] else 'NA'
        detail_dictionary["Phenoflow_id"] = int(detail['phenoflowid']) if detail['phenoflowid'] else 'NA'
        try:
            detail_dictionary["Data_sources"] = {item['name'] : item['url'] for item in detail['data_sources']} if 'url' in detail['data_sources'][0].keys() else 'NA'
        except: 
            detail_dictionary['Data_sources'] = 'NA'
        detail_dictionary["Coding_system"] = detail['coding_system'][0]["name"] if detail['coding_system'] else 'NA'
        detail_dictionary['Event_start_date'],detail_dictionary['Event_end_date'] = date_extract(detail['event_date_range']) 
        detail_dictionary["Status"] = int(detail["status"]) if detail["status"] else 'NA'
        detail_dictionary["Is_deleted"] = detail["is_deleted"] if detail["is_deleted"] else 'NA'
        detail_dictionary["Owner"] = detail["owner"] if detail["owner"] else 'NA'
        
        hdruk_detail.append(detail_dictionary)   

    sorted_detail = sorted(hdruk_detail,key=lambda x:x['Phenotype_id'])
    i = 0
    for detail in sorted_detail:
        i+=1
        detail['PID'] = f'HP{i:06d}'

    return sorted_detail


def get_concept(hdruk,detail):
    hdruk_concept = []
    id_list = []
    codelist = [data['codelist'] for data in hdruk]

    for data in codelist:
        for dic in data:
            if dic["id"] not in id_list:
                concept_dictionary = {}
                id_list.append(dic["id"])
                concept_dictionary["Description"] = dic['description'].strip().replace("\\", "")
                concept_dictionary["ID"] = dic["id"]
                concept_dictionary["Concept_id"] = [dic['concept_id']]
                concept_dictionary["Concept_history_id"] = [dic['concept_history_id']]
                concept_dictionary["Concept_history_date"] = [dic['concept_history_date']]
                concept_dictionary["Component_id"] = [dic["component_id"]]
                concept_dictionary["Component_history_id"] = [dic["component_history_id"]]
                concept_dictionary["Logical_type"] = [dic["logical_type"]]
                concept_dictionary["Codelist_id"] = [dic["codelist_id"]]
                concept_dictionary["Codelist_history_id"] = [dic["codelist_history_id"]]
                concept_dictionary["Code"] = [dic["code"]]
                concept_dictionary["Coding_system_id"] = [dic["coding_system"]["id"]]
                concept_dictionary["Coding_system_name"] = [dic["coding_system"]["name"]]
                concept_dictionary["Coding_system_description"] =  [dic["coding_system"]["description"]]
                concept_dictionary["Phenotype_id"] = [dic["phenotype_id"]]
                concept_dictionary["Phenotype_version_id"] = [dic["phenotype_version_id"]]
                concept_dictionary["Phenotype_name"] = [dic["phenotype_name"]]
                concept_dictionary["PIDs"] = [P["PID"] for P in detail if P['Phenotype_id'] == dic["phenotype_id"]]
                hdruk_concept.append(concept_dictionary)
            else:
                for concept in hdruk_concept:
                    if concept['ID'] == dic["id"]:
                        concept['Concept_id'].append(dic['concept_id']) 
                        concept['Concept_history_id'].append(dic['concept_history_id'])
                        concept['Concept_history_date'].append(dic['concept_history_date'])
                        concept['Component_id'].append(dic['component_id'])
                        concept['Component_history_id'].append(dic['component_history_id'])
                        concept['Logical_type'].append(dic['logical_type'])
                        concept['Codelist_id'].append(dic['codelist_id'])
                        concept['Codelist_history_id'].append(dic['codelist_history_id'])
                        concept['Code'].append(dic['code'])
                        concept['Coding_system_id'].append(dic['coding_system']['id'])
                        concept['Coding_system_name'].append(dic['coding_system']['name'])
                        concept['Coding_system_description'].append(dic['coding_system']['description'])
                        concept['Phenotype_id'].append(dic['phenotype_id'])
                        concept['Phenotype_version_id'].append(dic['phenotype_version_id'])
                        concept['Phenotype_name'].append(dic['phenotype_name'])
                        concept['PIDs'].extend([P["PID"] for P in detail if P['Phenotype_id'] == dic["phenotype_id"]])

    concept_sorted = sorted(hdruk_concept,key = lambda x: x['Description'])
    i = 0
    for concept in concept_sorted:
        i += 1
        concept['CID'] = f'HC{i:06d}'

    return concept_sorted
