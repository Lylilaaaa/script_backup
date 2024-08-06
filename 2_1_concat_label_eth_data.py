import json
from datetime import datetime, timedelta
from tqdm import tqdm
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def convert_to_normal_slash(path):
    return path.replace("\\", "/")

def to_addr(hex_str: str) -> str:
    return "0x" + hex_str[26:]

def to_date_norUTC (input_str: str) -> str:
    return input_str[:-4]

def set_meme_index():
    eth_meme_path = convert_to_normal_slash("D:\\Research_PostGraduate\\web3\\tweet\\outputs\\coinmarketcap_detail_Ethereum_final.csv")
    df = pd.read_csv(eth_meme_path, encoding='latin-1')
    df['meme_id'] = range(1, len(df) + 1)
    df.to_csv("D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum_final_indexed.csv", index=False)

# set_meme_index()


def find_rug_pull_eth():
    eth_meme_path = convert_to_normal_slash("D:\\Research_PostGraduate\\web3\\tweet\\outputs\\coinmarketcap_detail_Ethereum_final_indexed.csv")
    eth_df = pd.read_csv(eth_meme_path, encoding='latin-1') # Name, Rugpull_comfirm
    rugpull_meme_df = eth_df[eth_df['Rugpull_comfirm'] == 1]
    print(rugpull_meme_df["Name"])
    for file in tqdm(os.listdir("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data"), desc="Processing unique topics"):
        if file.endswith(".csv"): 
            meme_name = os.path.splitext(file)[0]
            if meme_name in rugpull_meme_df["Name"].values:
                source_file_path = os.path.join("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data", file)
                target_file_path = os.path.join("D:/Research_PostGraduate/web3/tweet/alldata/0_rugpull_confirm", file)
                os.rename(source_file_path, target_file_path)

# find_rug_pull_eth()

def read_dfs(data_path,label):
    # eth_meme_path = convert_to_normal_slash("D:\\Research_PostGraduate\\web3\\tweet\\outputs\\coinmarketcap_detail_Ethereum_final_indexed.csv")
    # eth_df = pd.read_csv(eth_meme_path, encoding='latin-1') # Name, Rugpull_comfirm
    result_dfs = []
    for file in tqdm(os.listdir(data_path), desc="Processing unique topics"):
        if file.endswith(".csv"): 
            file_path = os.path.join(data_path, file) 
            df = pd.read_csv(file_path)  # blockNumber,transactionIndex,logIndex,blockHash,transactionHash,timestamp,date,address,topic0,topic1,topic2,topic3,data,event_txt
            df = df.astype(str)
            meme_cate = os.path.splitext(file)[0]
            df['meme_cate'] = meme_cate
            df['topic1'] = df['topic1'].fillna('0x0000000000000000000000000000000000000000000000000000000000000000')
            df['topic2'] = df['topic2'].fillna('0x0000000000000000000000000000000000000000000000000000000000000000')
            # TODO: 将time变成秒的形式，对齐所有meme project的起始时间！！！！！！！！
            df['topic1'] = df['topic1'].apply(to_addr)
            df['topic2'] = df['topic2'].apply(to_addr)
            df['date'] = df['date'].str.replace(' UTC', '')
            df['date'] = pd.to_datetime(df['date'])
            first_date = df['date'].min()
            end_date = first_date + pd.Timedelta(days=30)
            df = df[(df['date'] >= first_date) & (df['date'] < end_date)]
            df['time_sec'] = (df['date'] - first_date).dt.total_seconds()
            df = df.assign(rugpull_label=lambda x: label)
            result_dfs.append(df)
    
    merged_df = pd.concat(result_dfs)
    merged_df.reset_index(drop=True)
    # merged_df['date'] = pd.to_datetime(merged_df['date'], format='%Y-%m-%d %H:%M:%S')
    merged_df = merged_df.sort_values(by='time_sec', ascending=True)
    merged_df.reset_index(drop=True)
    merged_df.to_csv('D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/0_meme_trans.csv', index=False)
# read_dfs("D:/Research_PostGraduate/web3/tweet/alldata/0_rugpull_pool_confirm",1)


    
def fix_dfs(data_path):
    df = pd.read_csv(data_path) # Name, Rugpull_comfirm
    df = df.drop('event_txt', axis=1)
    # df = df.drop('timestamp', axis=1)
    df = df.drop('blockHash', axis=1)
    df = df.drop('transactionHash', axis=1)
    # df = df.drop('rugpull_label', axis=1)
    df.to_csv(data_path, index=False)
# fix_dfs('D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/0_meme_trans.csv')

def merge_nor_rugpull_trans():
    nor_df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/0_meme_trans_nor.csv") # Name, Rugpull_comfirm
    rugpull_df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/0_meme_trans.csv") # Name, Rugpull_comfirm
    merged_df = pd.concat([nor_df, rugpull_df])
    merged_df.reset_index(drop=True)
    merged_df = merged_df.sort_values(by='time_sec', ascending=True)
    merged_df.reset_index(drop=True)
    merged_df.to_csv("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/meme_eth.csv", index=False)
# merge_nor_rugpull_trans()

def hash_function(text):
    return hash(text) & 0xFFFFFFFF

def merge_meme_index():
    df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/meme_eth.csv") # Name, Rugpull_comfirm
    df['meme_cate_hashed'] = df['meme_cate'].apply(hash_function)
    print(df['meme_cate_hashed'].value_counts())
    df = df.drop('meme_cate', axis=1)
    df.to_csv("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/meme_eth.csv", index=False)
    


def hex_meme_index():
    df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/meme_eth.csv") # Name, Rugpull_comfirm
    cols_to_convert = ['address', 'topic0', 'topic1', 'topic2', 'topic3', 'data']
    df.fillna(0, inplace=True)
    for col in cols_to_convert:
        hex_values = df[col].tolist()
        int_values = []
        for hex_value in hex_values:
            if isinstance(hex_value, int):
                int_values.append(hex_value)
            elif isinstance(hex_value, str) and hex_value[2:].strip() != '':
                int_values.append(int(hex_value[2:], 16))
            elif isinstance(hex_value, str) and hex_value[2:].strip() == '':
                int_values.append(int(0))
        df[col] = int_values
    for col in cols_to_convert:
        int_values = df[col].tolist()
        int_simple_values = []
        for int_value in int_values:
            int_simple_values.append(int(int_value) % (2**31 - 1))
        df[col] = int_simple_values
    df.to_csv("D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/meme_eth.csv", index=False)
# merge_meme_index()
# hex_meme_index()



def get_nodes_from_edges(edge_csv_path, output_csv_path):
    edge_df = pd.read_csv(edge_csv_path)
    rugpull_df = edge_df[edge_df['rugpull_label'] == 1]
    rugpull_node_df = pd.concat([rugpull_df['topic1'], rugpull_df['topic2']], ignore_index=True)
    unique_rugpull_node_df = rugpull_node_df.drop_duplicates().reset_index(drop=True)
    rugpull_node_info = pd.DataFrame({
        'addr': unique_rugpull_node_df,
        'rugpull_label': 1
    })
    print(len(rugpull_node_info))
    nor_df = edge_df[edge_df['rugpull_label'] == 0]
    nor_node_df = pd.concat([nor_df['topic1'], nor_df['topic2']], ignore_index=True)
    unique_nor_node_df = nor_node_df.drop_duplicates().reset_index(drop=True)
    nor_node_info = pd.DataFrame({
        'addr': unique_nor_node_df,
        'rugpull_label': 0
    })
    common_addrs = rugpull_node_info['addr'].unique()
    init = len(nor_node_info)
    print(len(nor_node_info))
    nor_node_info_sep = nor_node_info[~nor_node_info['addr'].isin(common_addrs)]
    print(init-len(nor_node_info_sep))
    merged_node_info = pd.concat([rugpull_node_info, nor_node_info_sep], ignore_index=True)
    common_addrs = pd.merge(rugpull_node_info, nor_node_info, on='addr', how='inner')['addr'].unique()
    print(len(common_addrs))
    # 创建 mask 列
    merged_node_info['mask'] = 0
    merged_node_info.loc[merged_node_info['addr'].isin(common_addrs), 'mask'] = 1
    merged_node_info.to_csv(output_csv_path, index=False)

get_nodes_from_edges('D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/meme_eth.csv', 'D:/Research_PostGraduate/web3/tweet/alldata/preparing_data1/meme_eth_node.csv')