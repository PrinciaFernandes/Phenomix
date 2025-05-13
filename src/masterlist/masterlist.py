

def transform_detail(detail_files):
    new_detail = []
    for dict in detail_files:
        d = {}
        if 'Outcome' in dict.keys(): 
            d['Name'] = dict['Outcome']
        elif 'Disease' in dict.keys():
            d['Name'] = dict['Disease']
        elif "Cohort_name" in dict.keys():
            d['Name'] = dict["Cohort_name"]
        else:
            d['Name'] = dict['Name']
        if 'PID' in dict.keys():
            d['PID'] = dict['PID']
        new_detail.append(d)
    return new_detail


def get_pid_key(pid):
    keys = ['Phenotypes','hdruk_PID','phekb_PID','cprd_PID','Sentinel_PID','ohdsi_PID']
    key_map = {'H':keys[1],'P':keys[2],'C':keys[3],'S':keys[4],'O':keys[5]}
    init_pid = pid[0]
    if init_pid in key_map:
        return key_map[init_pid]


def create_masterlist(combined_detail):
    masterlist = []
    name_list = []
    keys = ['Phenotypes','hdruk_PID','phekb_PID','cprd_PID','Sentinel_PID','ohdsi_PID']

    for detail in combined_detail:
        if detail['Name'] not in name_list:
            name_list.append(detail['Name'])
            d = {k:None for k in keys}
            d[keys[0]] = detail['Name']
            pid_key = get_pid_key(detail['PID'])
            d[pid_key] = detail['PID']
            masterlist.append(d)
        else:

            pid_key = get_pid_key(detail['PID'])
            for d in masterlist:
                if d[keys[0]] == detail['Name']:
                    if not d[pid_key] is None:
                        d[pid_key] = d[pid_key] + f', {detail['PID']}' 
                    else:
                        d[pid_key] = detail['PID']
    sorted_masterlist = sorted(masterlist,key = lambda x:x['Phenotypes'])
    id = 0
    for d in sorted_masterlist:
        id += 1
        
        v1 = 'H' if d['hdruk_PID'] is not None else 'X'
        v2 = 'P' if d['phekb_PID'] is not None else 'X'
        v3 = 'C' if d['cprd_PID'] is not None else 'X'
        v4 = 'S' if d['Sentinel_PID'] is not None else 'X'
        v5 = 'O' if d['ohdsi_PID'] is not None else 'X'

        d['id'] = f'{v1}{v2}{v3}{v4}{v5}{id:04d}'
    
    return sorted_masterlist


