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
        detail_dictionary["Phenotype_id"] = detail.get('phenotype_id',"NA")
        detail_dictionary["Phenotype_version_id"] = int(detail.get('phenotype_version_id',"NA"))
        detail_dictionary["Name"] = detail.get('name',"NA")
        detail_dictionary["Defination"] = detail.get('definition',"NA")
        detail_dictionary["Implementation"] = detail.get('implementation',"NA")
        detail_dictionary["Publications"] = detail.get('publications',"NA")
        detail_dictionary["Validation"] = detail.get("validation","NA")
        detail_dictionary["Citation_requirements"] = detail.get("citation_requirements","NA")
        detail_dictionary["Created"] = detail.get("created","NA")
        detail_dictionary["author"] = detail.get("author","NA")
        detail_dictionary["Collections"] = [item['name'] for item in detail.get('collections', [])]
        detail_dictionary["Tags"] = detail.get("tags","NA")
        detail_dictionary["Group"] = detail.get("group","NA")
        detail_dictionary["Group_access"] = int(detail.get("group_access","NA"))
        detail_dictionary["World_access"] = int(detail.get("world_access","NA"))
        detail_dictionary["Updated"] = detail.get("updated","NA")
        detail_dictionary["Sex"] = detail.get('sex', [{}])[0].get("name","NA")
        detail_dictionary["Type"] = detail.get('type', [{}])[0].get("name","NA")
        detail_dictionary["Phenoflow_id"] = int(detail.get('phenoflowid',"NA"))
        try:
            detail_dictionary["Data_sources"] = {item['name'] : item['url'] for item in detail['data_sources']} if 'url' in detail['data_sources'][0].keys() else 'NA'
        except: 
            detail_dictionary['Data_sources'] = 'NA'
        detail_dictionary["Coding_system"] = detail['coding_system'][0]["name"] if detail['coding_system'] else 'NA'
        detail_dictionary['Event_start_date'],detail_dictionary['Event_end_date'] = date_extract(detail.get('event_date_range',"NA")) 
        detail_dictionary["Status"] = int(detail.get("status","NA"))
        detail_dictionary["Is_deleted"] = detail.get("is_deleted","NA")
        detail_dictionary["Owner"] = detail.get("owner","NA")

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
                concept_dictionary["ID"] = dic.get("id", "NA")
                concept_dictionary["Concept_id"] = [dic.get('concept_id', "NA")]
                concept_dictionary["Concept_history_id"] = [dic.get('concept_history_id', "NA")]
                concept_dictionary["Concept_history_date"] = [dic.get('concept_history_date', "NA")]
                concept_dictionary["Component_id"] = [dic.get("component_id", "NA")]
                concept_dictionary["Component_history_id"] = [dic.get("component_history_id", "NA")]
                concept_dictionary["Logical_type"] = [dic.get("logical_type", "NA")]
                concept_dictionary["Codelist_id"] = [dic.get("codelist_id", "NA")]
                concept_dictionary["Codelist_history_id"] = [dic.get("codelist_history_id", "NA")]
                concept_dictionary["Code"] = [dic.get("code", "NA")]
                concept_dictionary["Coding_system_id"] = [dic.get("coding_system", {}).get("id", "NA")]
                concept_dictionary["Coding_system_name"] = [dic.get("coding_system", {}).get("name", "NA")]
                concept_dictionary["Coding_system_description"] =  [dic.get("coding_system", {}).get("description", "NA")]
                concept_dictionary["Phenotype_id"] = [dic.get("phenotype_id", "NA")]
                concept_dictionary["Phenotype_version_id"] = [dic.get("phenotype_version_id", "NA")]
                concept_dictionary["Phenotype_name"] = [dic.get("phenotype_name", "NA")]
                concept_dictionary["PIDs"] = [item["PID"] for item in detail if item['Phenotype_id'] == dic["phenotype_id"]]
                hdruk_concept.append(concept_dictionary)
            else:
                for concept in hdruk_concept:
                    if concept['ID'] == dic["id"]:
                        concept['Concept_id'].append(dic.get('concept_id', "NA"))
                        concept['Concept_history_id'].append(dic.get('concept_history_id', "NA"))
                        concept['Concept_history_date'].append(dic.get('concept_history_date', "NA"))
                        concept['Component_id'].append(dic.get('component_id', "NA"))
                        concept['Component_history_id'].append(dic.get('component_history_id', "NA"))
                        concept['Logical_type'].append(dic.get('logical_type', "NA"))
                        concept['Codelist_id'].append(dic.get('codelist_id', "NA"))
                        concept['Codelist_history_id'].append(dic.get('codelist_history_id', "NA"))
                        concept['Code'].append(dic.get('code', "NA"))
                        concept['Coding_system_id'].append(dic.get('coding_system', {}).get('id', "NA"))
                        concept['Coding_system_name'].append(dic.get('coding_system', {}).get('name', "NA"))
                        concept['Coding_system_description'].append(dic.get('coding_system', {}).get('description', "NA"))
                        concept['Phenotype_id'].append(dic.get('phenotype_id', "NA"))
                        concept['Phenotype_version_id'].append(dic.get('phenotype_version_id', "NA"))
                        concept['Phenotype_name'].append(dic.get('phenotype_name', "NA"))
                        concept['PIDs'].extend([item["PID"] for item in detail if item['Phenotype_id'] == dic["phenotype_id"]])

    concept_sorted = sorted(hdruk_concept,key = lambda x: x['Description'])
    i = 0
    for concept in concept_sorted:
        i += 1
        concept['CID'] = f'HC{i:06d}'

    return concept_sorted
