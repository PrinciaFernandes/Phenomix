
def get_detail(cprd):
    i = 0
    hdruk_detail = []
    disease_list = []
    for pheno in cprd:
        if pheno['disease'] not in disease_list:
            disease_list.append(pheno['disease'])
            i += 1
            detail_dictionary = {}
            detail_dictionary['Disease'] = pheno['disease']
            detail_dictionary['Disease_num'] = pheno['disease_num']
            detail_dictionary['PID'] = f'CP{i:06d}'
            hdruk_detail.append(detail_dictionary)
    return hdruk_detail



def get_concept(cprd,detail):
    hdruk_concept = []
    disease_code_list = []
    for pheno in cprd:
        if pheno['read code'] not in disease_code_list:
            concept_dctionary = {}
            disease_code_list.append(pheno['read code'])
            concept_dctionary['Read_code'] = str(pheno['read code'])
            concept_dctionary['Description'] = pheno['descr']
            concept_dctionary['Med_code'] = [pheno['medcode']]
            concept_dctionary['Category'] = [pheno['category']]
            concept_dctionary['System'] = [pheno['system']]
            concept_dctionary['System_num'] = [pheno['system_num']]
            concept_dctionary['Med_code_id'] = [pheno['medcodeid']]
            concept_dctionary['Snomed_ct_concept_id'] = [pheno['snomedctconceptid']]
            concept_dctionary['Snomed_ct_description_id'] = [pheno['snomedctdescriptionid']]
            concept_dctionary['Mapping'] = [pheno['mapping']]
            concept_dctionary['Disease'] = [pheno['disease']]
            concept_dctionary['Disease_num'] = [pheno['disease_num']]
            concept_dctionary['PIDs'] = [dict['PID'] for dict in detail if dict['Disease'] == pheno['disease']]
            hdruk_concept.append(concept_dctionary)

        else: 
            for concept in hdruk_concept: 
                if concept['Disease'] == pheno['disease']:
                    concept['Med_code'].append(pheno['medcode']) 
                    concept['Category'].append(pheno['category'])
                    concept['System'].append(pheno['system'])
                    concept['System_num'].append(pheno['system_num']) 
                    concept['Med_code_id'].append(pheno['medcodeid'])
                    concept['Snomed_ct_concept_id'].append(pheno['snomedctconceptid']) 
                    concept['Snomed_ct_description_id'].append(pheno['snomedctdescriptionid']) 
                    concept['Mapping'].append(pheno['mapping']) 
                    concept['Disease'].append(pheno['disease']) 
                    concept['Disease_num'].append(pheno['disease_num']) 
                    concept['PIDs'].extend([dict['PID'] for dict in detail if dict['Disease'] == pheno['Disease']])

    sorted_concept = sorted(hdruk_concept,key = lambda x: x['Read_code'])
    i = 0
    for concept in sorted_concept:
        i += 1
        concept['CID'] = f'CC{i:06d}'

    return sorted_concept
