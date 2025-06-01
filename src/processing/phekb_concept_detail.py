
def get_detail(phekb):
    phekb_detail = phekb
    i = 0
    for detail in phekb_detail:
        i += 1
        detail['Phenotype_id'] = int(detail['Phenotype_id'])
        detail['PID'] = f'PP{i:06d}'
    return phekb_detail

def get_concept(phekb,detail):
    phekb_concept = []
    i = 0
    for item_data in phekb:
        i += 1
        concept_json = {}
        concept_json['Files'] = item_data.get('Files','NA')
        concept_json['Phenotype_attributes'] = item_data.get('Phenotype_attributes', 'NA')
        concept_json['Phenotype_id'] = item_data.get('Phenotype_id', 'NA')
        concept_json['Name'] = item_data.get('Name', 'NA')
        concept_json['PIDs'] = [dict['PID'] for dict in detail if dict['Phenotype_id'] == item_data['Phenotype_id']]
        concept_json['CID'] = f'PC{i:06d}'
        phekb_concept.append(concept_json)
    return phekb_concept
    

