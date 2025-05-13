
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
    for data in phekb:
        i += 1
        concept_json = {}
        concept_json['Files'] = data['Files']
        concept_json['Phenotype_attributes'] = data['Phenotype_attributes']
        concept_json['Phenotype_id'] = data['Phenotype_id']
        concept_json['Name'] = data['Name']
        concept_json['PIDs'] = [dict['PID'] for dict in detail if dict['Phenotype_id'] == data['Phenotype_id']]
        concept_json['CID'] = f'PC{i:06d}'
        phekb_concept.append(concept_json)
    return phekb_concept
    

