import requests
import pandas as pd


def cprd_scrapping(base_url:str):
    cprd = []
    csv_files = []
    response = requests.get(base_url)
    files = response.json()

    for file in files:
        if file['name'].endswith('.csv'):
            csv_files.append(file['download_url'])

    i = 0
    for file in csv_files:
        i += 1
        cprd_df = pd.read_csv(file,  na_values=['','NA'], keep_default_na=False)
        if not cprd_df.empty:
            cprd_df['read code'] = cprd_df['read code'].fillna(cprd_df['snomedctdescriptionid'])

            print(f'{i}:{file}')
            for row in cprd_df.values.tolist():
                cprd_dictionary = {}
                for col,val in zip(cprd_df.columns,row):
                    cprd_dictionary[col] = val
                cprd.append(cprd_dictionary)
    return cprd
