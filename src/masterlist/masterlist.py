

def transform_detail(detail_files:list)->list:
    new_detail = []
    for dict in detail_files:
        detail_dict = {}
        if 'Outcome' in dict.keys(): 
            detail_dict['Name'] = dict['Outcome']
        elif 'Disease' in dict.keys():
            detail_dict['Name'] = dict['Disease']
        elif "Cohort_name" in dict.keys():
            detail_dict['Name'] = dict["Cohort_name"]
        else:
            detail_dict['Name'] = dict['Name']
        if 'PID' in dict.keys():
            detail_dict['PID'] = dict['PID']
        new_detail.append(detail_dict  )
    return new_detail


def get_pid_key(pid:str)->str:
    keys = ['Phenotypes','hdruk_PID','phekb_PID','cprd_PID','Sentinel_PID','ohdsi_PID']
    key_map = {'H':keys[1],'P':keys[2],'C':keys[3],'S':keys[4],'O':keys[5]}
    init_pid = pid[0]
    if init_pid in key_map:
        return key_map[init_pid]


def create_masterlist(combined_detail:list)->list:
    masterlist = []
    name_list = []
    keys = ['Phenotypes','hdruk_PID','phekb_PID','cprd_PID','Sentinel_PID','ohdsi_PID']

    for detail in combined_detail:
        if detail['Name'] not in name_list:
            name_list.append(detail['Name'])
            detail_dict = {key:None for key in keys}
            detail_dict[keys[0]] = detail['Name']
            pid_key = get_pid_key(detail['PID'])
            detail_dict[pid_key] = detail['PID']
            masterlist.append(detail_dict)
        else:

            pid_key = get_pid_key(detail['PID'])
            for dict in masterlist:
                if dict[keys[0]] == detail['Name']:
                    if not dict[pid_key] is None:
                        dict[pid_key] = dict[pid_key] + f', {detail["PID"]}' 
                    else:
                        dict[pid_key] = detail['PID']
    sorted_masterlist = sorted(masterlist, key=lambda x:x['Phenotypes'])
    id = 0
    for dict in sorted_masterlist:
        id += 1

        v1 = 'H' if dict['hdruk_PID'] is not None else 'X'
        v2 = 'P' if dict['phekb_PID'] is not None else 'X'
        v3 = 'C' if dict['cprd_PID'] is not None else 'X'
        v4 = 'S' if dict['Sentinel_PID'] is not None else 'X'
        v5 = 'O' if dict['ohdsi_PID'] is not None else 'X'

        dict['id'] = f'{v1}{v2}{v3}{v4}{v5}{id:04d}'

    return sorted_masterlist


