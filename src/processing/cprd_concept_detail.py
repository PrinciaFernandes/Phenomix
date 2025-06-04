
def get_detail(cprd:list)->list:
    i = 0
    hdruk_detail = []
    disease_list = []
    for pheno in cprd:
        if pheno.get('disease') not in disease_list:
            disease_list.append(pheno.get('disease', 'Unknown'))
            i += 1
            detail_dictionary = {}
            detail_dictionary['Disease'] = pheno.get('disease','Unknown')
            detail_dictionary['Disease_num'] = pheno.get('disease_num','Unknown')
            detail_dictionary['PID'] = f'CP{i:06d}'
            hdruk_detail.append(detail_dictionary)
        else:
            continue
    return hdruk_detail



def get_concept(cprd:list,detail:list)->list:
    hdruk_concept = []
    disease_code_list = []
    for pheno in cprd:
        if pheno.get('read code') not in disease_code_list:
            concept_dctionary = {}
            disease_code_list.append(pheno.get('read code',None))
            concept_dctionary['Read_code'] = str(pheno.get('read code',None))
            concept_dctionary['Description'] = pheno.get('descr',None)
            concept_dctionary['Med_code'] = [pheno.get('medcode', None)]
            concept_dctionary['Category'] = [pheno.get('category', None)]
            concept_dctionary['System'] = [pheno.get('system', None)]
            concept_dctionary['System_num'] = [pheno.get('system_num', None)]
            concept_dctionary['Med_code_id'] = [pheno.get('medcodeid', None)]
            concept_dctionary['Snomed_ct_concept_id'] = [pheno.get('snomedctconceptid', None)]
            concept_dctionary['Snomed_ct_description_id'] = [pheno.get('snomedctdescriptionid', None)]
            concept_dctionary['Mapping'] = [pheno.get('mapping', None)]
            concept_dctionary['Disease'] = [pheno.get('disease', None)]
            concept_dctionary['Disease_num'] = [pheno.get('disease_num', None)]
            concept_dctionary['PIDs'] = [dict.get('PID') for dict in detail if dict.get('Disease') == pheno.get('disease', None)]
            hdruk_concept.append(concept_dctionary)

        else: 
            for concept in hdruk_concept: 
                if concept['Disease'] == pheno['disease']:
                    concept['Med_code'].append(pheno.get('medcode', None)) 
                    concept['Category'].append(pheno.get('category', None))
                    concept['System'].append(pheno.get('system', None))
                    concept['System_num'].append(pheno.get('system_num', None)) 
                    concept['Med_code_id'].append(pheno.get('medcodeid', None))
                    concept['Snomed_ct_concept_id'].append(pheno.get('snomedctconceptid', None)) 
                    concept['Snomed_ct_description_id'].append(pheno.get('snomedctdescriptionid', None)) 
                    concept['Mapping'].append(pheno.get('mapping', None)) 
                    concept['Disease'].append(pheno.get('disease', None)) 
                    concept['Disease_num'].append(pheno.get('disease_num', None)) 
                    concept['PIDs'].extend([dict['PID'] for dict in detail if dict['Disease'] == pheno['Disease']])

    sorted_concept = sorted(hdruk_concept,key = lambda x: x['Read_code'])
    i = 0
    for concept in sorted_concept:
        i += 1
        concept['CID'] = f'CC{i:06d}'

    return sorted_concept
