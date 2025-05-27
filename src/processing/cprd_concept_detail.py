
def get_detail(cprd):
    i = 0
    hdruk_detail = []
    disease_list = []
    for pheno in cprd:
        if pheno['disease'] not in disease_list:
            disease_list.append(pheno.get('disease',None))
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
            disease_code_list.append(pheno.get('read code',""))
            concept_dctionary['Read_code'] = str(pheno.get('read code',""))
            concept_dctionary['Description'] = pheno.get('descr',"NA")
            concept_dctionary['Med_code'] = [pheno.get('medcode',"NA")]
            concept_dctionary['Category'] = [pheno.get('category',"NA")]
            concept_dctionary['System'] = [pheno.get('system',"NA")]
            concept_dctionary['System_num'] = [pheno.get('system_num',"NA")]
            concept_dctionary['Med_code_id'] = [pheno.get('medcodeid',"NA")]
            concept_dctionary['Snomed_ct_concept_id'] = [pheno.get('snomedctconceptid',"NA")]
            concept_dctionary['Snomed_ct_description_id'] = [pheno.get('snomedctdescriptionid',"NA")]
            concept_dctionary['Mapping'] = [pheno.get('mapping',"NA")]
            concept_dctionary['Disease'] = [pheno.get('disease',"NA")]
            concept_dctionary['Disease_num'] = [pheno.get('disease_num',"NA")]
            concept_dctionary['PIDs'] = [dict['PID'] for dict in detail if dict['Disease'] == pheno['disease']]
            hdruk_concept.append(concept_dctionary)

        else: 
            for concept in hdruk_concept: 
                if concept['Disease'] == pheno['disease']:
                    concept['Med_code'].append(pheno.get('medcode',"NA")) 
                    concept['Category'].append(pheno.get('category',"NA"))
                    concept['System'].append(pheno.get('system',"NA"))
                    concept['System_num'].append(pheno.get('system_num',"NA")) 
                    concept['Med_code_id'].append(pheno.get('medcodeid',"NA"))
                    concept['Snomed_ct_concept_id'].append(pheno.get('snomedctconceptid',"NA")) 
                    concept['Snomed_ct_description_id'].append(pheno.get('snomedctdescriptionid',"NA")) 
                    concept['Mapping'].append(pheno.get('mapping',"NA")) 
                    concept['Disease'].append(pheno.get('disease',"NA")) 
                    concept['Disease_num'].append(pheno.get('disease_num',"NA")) 
                    concept['PIDs'].extend([dict['PID'] for dict in detail if dict['Disease'] == pheno['Disease']])

    sorted_concept = sorted(hdruk_concept,key = lambda x: x['Read_code'])
    i = 0
    for concept in sorted_concept:
        i += 1
        concept['CID'] = f'CC{i:06d}'

    return sorted_concept
