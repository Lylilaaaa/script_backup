import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
from tqdm import tqdm
def get_event_signature(hex_signature):
    url = 'https://www.4byte.directory/api/v1/event-signatures/'
    params = {'hex_signature': hex_signature}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]
        else:
            return {'id': 000, 'created_at': '2024-04-13T22:38:00.801049Z', 'text_signature': 'No_match', 'hex_signature': '0x00000', 'bytes_signature': 'none'}
    else:
        return {'id': 0000, 'created_at': '2024-04-13T22:38:00.801049Z', 'text_signature': 'No_match_sub', 'hex_signature': '0x000000', 'bytes_signature': 'none_sub'}

# add signature to each topics0
new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/0_nor_pool_confirm"  
signature_dict = {}
signatures_list = []
count = 0

for root, dirs, files in os.walk(new_directory):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            df = pd.read_csv(file_path)
            if "event_txt" not in df.columns:
                topics0_list = df["topic0"]
                unique_topics0_list = list(set(topics0_list))
                for hex in tqdm(unique_topics0_list, desc="Processing unique topics"):
                    if hex not in signature_dict:
                        event_data = get_event_signature(hex)
                        event_data.pop('bytes_signature', None)
                        signature_dict[hex] = event_data['text_signature']
                        signatures_list.append(event_data)
                    else:
                        pass
                count+=1
                csv_filename = f'events_{count}.csv'
                df = pd.DataFrame(signatures_list)
                print(signatures_list)
                df.to_csv(csv_filename, index=False, encoding='utf-8', escapechar='\\')



