import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
from tqdm import tqdm

# for root, dirs, files in os.walk(new_directory):
#     for file in files:
#         if file.endswith(".csv"):
#             file_path = os.path.join(root, file)
#             df = pd.read_csv(file_path)


def event_data_add():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/0_nor_pool_confirm"
    event_path = "D:/Research_PostGraduate/web3/tweet/_events.csv"
    event_df = pd.read_csv(event_path) #id,created_at,text_signature,hex_signature,bytes_signature
    event_signature_to_name = event_df.set_index('hex_signature')['text_signature'].to_dict()
    for root, dirs, files in os.walk(new_directory):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                if "event_txt" not in df.columns:
                    df['event_txt'] = df['topic0'].map(event_signature_to_name)
                    df.to_csv(file_path, index=False, encoding='utf-8', escapechar='\\')
event_data_add()

def rug_pull_check():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata"
    eth_csv_path = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    eth_df =pd.read_csv(eth_csv_path)
    selected_data = eth_df[ (eth_df['Rugpull_level'] == 5)| (eth_df['Rugpull_level'] == 8)| (eth_df['Rugpull_level'] == 9)]
    print(selected_data)
# rug_pull_check()
# event_data_add()

def event_plot():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/rug_pull_not_comfirm"
    eth_csv_path = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    eth_df =pd.read_csv(eth_csv_path)
    for root, dirs, files in os.walk(new_directory):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                event_signatures = df['event_txt']
                event_signatures_clean = df['event_txt'].str.split('(').str[0]
                event_signature_counts = event_signatures_clean.value_counts()
                coin_name = os.path.splitext(file)[0]
                save_path = os.path.join(root, f"{coin_name}_event_plot.png")
                plt.figure(figsize=(15, 8))
                event_signature_counts.plot(kind='pie', autopct='%1.1f%%', labeldistance=1.1, startangle=140, pctdistance=0.85, counterclock=False , wedgeprops=dict(width=0.4))#, cmap='tab20c'
                plt.axis('equal')
                plt.legend(loc="center right")  # 将图例放置在图表外部
                plt.title(f'Event Signature Frequency of Token {coin_name}')
                plt.savefig(save_path)

# event_plot()
# event_data_add()