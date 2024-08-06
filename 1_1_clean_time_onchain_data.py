from Scweet.scweet import scrape
import pandas as pd
from tqdm import tqdm
import os
from datetime import datetime, timedelta
import time
from Scweet.scweet import scrape_certain_link
import shutil
import matplotlib.pyplot as plt
import numpy as np
def price_rug_combine():
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    eth_df = pd.read_csv(eth_dic)

    # 过滤出 price_drop 不为 None 的行
    filtered_df = eth_df.dropna(subset=['price_drop'])

    # 保存过滤后的数据框为新的 CSV 文件
    filtered_df.to_csv("D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum_with_price.csv", index=False)

# 调用函数
# price_rug_combine()

def plot_twitter_and_onchain(twitter_data, onchain_data, title1, title2, save_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # 绘制twitter数据
    twitter_data.plot(kind='bar', ax=ax1)
    ax1.set_title(title1)
    ax1.set_xlabel("Time Range")
    ax1.set_ylabel("Frequency")

    # 绘制on-chain数据
    onchain_data.plot(kind='bar', ax=ax2)
    ax2.set_title(title2)
    ax2.set_xlabel("Time Range")
    ax2.set_ylabel("Frequency")

    plt.savefig(save_path)



def clean_pool_data_base_on_twitter():
    twitter_folder_dic = "D:/Research_PostGraduate/web3/tweet/outputs/social_data_rug_pull"
    twitter_df_result = pd.DataFrame(columns=['big_coin_name', 'start_time', 'end_time'])
    cumulative_frequency_data = pd.Series()
    big_name_list = []
    for file in tqdm(os.listdir(twitter_folder_dic), desc="Processing twitter"):
        if file.endswith(".csv"):
            coin_name = os.path.splitext(file)[0]
            parts = coin_name.split("_")
            first_part = parts[0]
            big_coin_name = first_part[1:]
            print("big_coin_name: ", big_coin_name)
            big_name_list.append(big_coin_name)
            file_path = os.path.join(twitter_folder_dic, file)
            twi_df = pd.read_csv(file_path, encoding='ISO-8859-1')
            twi_df['Timestamp'] = pd.to_datetime(twi_df['Timestamp'])
            start_time = twi_df['Timestamp'].min()
            end_time = twi_df['Timestamp'].max()
            print(f"Time range: {start_time} to {end_time}")

            if big_coin_name in ["ELONIUM", "BUBS"]:
                continue
            try:
                data_to_append = {'big_coin_name': big_coin_name, 'start_time': start_time, 'end_time': end_time}
                df_to_append = pd.DataFrame([data_to_append])
                twitter_df_result = pd.concat([twitter_df_result, df_to_append], ignore_index=True)

                time_range = pd.date_range(start=start_time, end=end_time, periods=21)
                twi_df['TimeRange'] = pd.cut(twi_df['Timestamp'], bins=time_range)
                frequency_data = twi_df['TimeRange'].value_counts().sort_index()

                new_index = pd.Series()
                for i, interval in enumerate(frequency_data.index):
                    new_interval = pd.Interval(left=i*5, right=(i+1)*5, closed='right')
                    new_index.at[new_interval] = frequency_data[i]

                frequency_data.index = new_index.index

                total_count = frequency_data.sum()
                percentage_data = (frequency_data / total_count) * 100
                weighted_frequency_data = percentage_data * total_count
                cumulative_frequency_data = cumulative_frequency_data.add(weighted_frequency_data, fill_value=0)
                
            except Exception as e:
                print(f"Error processing {file}: {e}")
                continue

    twitter_df_result.to_csv('D:/Research_PostGraduate/web3/tweet/outputs/twitter_time_range_all.csv', index=False)

    total_count = cumulative_frequency_data.sum()
    percentage_cumulative_frequency_data = (cumulative_frequency_data / total_count) * 100
    print("Percentage cumulative frequency data:", percentage_cumulative_frequency_data)

    fig, ax = plt.subplots(figsize=(12, 10))
    percentage_cumulative_frequency_data.plot(kind='bar', ax=ax)
    ax.set_title(f"Tweet Frequency for all rug pull memecoin")
    ax.set_xlabel("Time Range")
    ax.set_ylabel("Frequency")
    plt.savefig(f"D:/Research_PostGraduate/web3/tweet/outputs/img/total_twi_fre.png")  # 保存为PNG文件
    print(big_name_list)
# clean_pool_data_base_on_twitter()


def pool_data_base_on_chain():
    twitter_folder_dic = "D:/Research_PostGraduate/web3/tweet/alldata/0_rugpull_pool_confirm"
    twitter_df_result = pd.DataFrame(columns=['small_coin_name', 'start_time', 'end_time'])
    cumulative_frequency_data = pd.Series()
    big_name_list = []
    for file in tqdm(os.listdir(twitter_folder_dic), desc="Processing twitter"):
        if file.endswith(".csv"):
            coin_name = os.path.splitext(file)[0]
            parts = coin_name.split("_")
            first_part = parts[0]
            big_coin_name = first_part
            print("small_coin_name: ", big_coin_name)
            big_name_list.append(big_coin_name)
            file_path = os.path.join(twitter_folder_dic, file)
            twi_df = pd.read_csv(file_path, encoding='ISO-8859-1')
            twi_df['date'] = pd.to_datetime(twi_df['date'])
            start_time = twi_df['date'].min()
            end_time = twi_df['date'].max()
            print(f"Time range: {start_time} to {end_time}")
            try:
                data_to_append = {'small_coin_name': big_coin_name, 'start_time': start_time, 'end_time': end_time}
                df_to_append = pd.DataFrame([data_to_append])
                twitter_df_result = pd.concat([twitter_df_result, df_to_append], ignore_index=True)

                time_range = pd.date_range(start=start_time, end=end_time, periods=21)
                twi_df['date'] = pd.cut(twi_df['date'], bins=time_range)
                frequency_data = twi_df['date'].value_counts().sort_index()

                new_index = pd.Series()
                for i, interval in enumerate(frequency_data.index):
                    new_interval = pd.Interval(left=i*5, right=(i+1)*5, closed='right')
                    new_index.at[new_interval] = frequency_data[i]

                frequency_data.index = new_index.index

                total_count = frequency_data.sum()
                percentage_data = (frequency_data / total_count) * 100
                weighted_frequency_data = percentage_data * total_count
                cumulative_frequency_data = cumulative_frequency_data.add(weighted_frequency_data, fill_value=0)
                
            except Exception as e:
                print(f"Error processing {file}: {e}")
                continue

    twitter_df_result.to_csv('D:/Research_PostGraduate/web3/tweet/outputs/onchain_time_range_all.csv', index=False)

    total_count = cumulative_frequency_data.sum()
    percentage_cumulative_frequency_data = (cumulative_frequency_data / total_count) * 100
    print("Percentage cumulative frequency data:", percentage_cumulative_frequency_data)

    fig, ax = plt.subplots(figsize=(12, 10))
    percentage_cumulative_frequency_data.plot(kind='bar', ax=ax)
    ax.set_title(f"Transaction Frequency for all rug pull memecoin")
    ax.set_xlabel("Time Range")
    ax.set_ylabel("Frequency")
    plt.savefig(f"D:/Research_PostGraduate/web3/tweet/outputs/img/total_trans_fre.png")  # 保存为PNG文件
    print(big_name_list)
# pool_data_base_on_chain()


def pool_data_base_on_chain_nor():
    twitter_folder_dic = "D:/Research_PostGraduate/web3/tweet/alldata/0_nor_pool_confirm"
    twitter_df_result = pd.DataFrame(columns=['small_coin_name', 'start_time', 'end_time'])
    cumulative_frequency_data = pd.Series()
    big_name_list = []
    for file in tqdm(os.listdir(twitter_folder_dic), desc="Processing twitter"):
        if file.endswith(".csv"):
            coin_name = os.path.splitext(file)[0]
            parts = coin_name.split("_")
            first_part = parts[0]
            big_coin_name = first_part
            print("small_coin_name: ", big_coin_name)
            big_name_list.append(big_coin_name)
            file_path = os.path.join(twitter_folder_dic, file)
            twi_df = pd.read_csv(file_path, encoding='ISO-8859-1')
            twi_df['date'] = pd.to_datetime(twi_df['date'])
            start_time = twi_df['date'].min()
            end_time = twi_df['date'].max()
            print(f"Time range: {start_time} to {end_time}")
            try:
                data_to_append = {'small_coin_name': big_coin_name, 'start_time': start_time, 'end_time': end_time}
                df_to_append = pd.DataFrame([data_to_append])
                twitter_df_result = pd.concat([twitter_df_result, df_to_append], ignore_index=True)

                time_range = pd.date_range(start=start_time, end=end_time, periods=21)
                twi_df['date'] = pd.cut(twi_df['date'], bins=time_range)
                frequency_data = twi_df['date'].value_counts().sort_index()

                new_index = pd.Series()
                for i, interval in enumerate(frequency_data.index):
                    new_interval = pd.Interval(left=i*5, right=(i+1)*5, closed='right')
                    new_index.at[new_interval] = frequency_data[i]

                frequency_data.index = new_index.index

                total_count = frequency_data.sum()
                percentage_data = (frequency_data / total_count) * 100
                weighted_frequency_data = percentage_data * total_count
                cumulative_frequency_data = cumulative_frequency_data.add(weighted_frequency_data, fill_value=0)
                
            except Exception as e:
                print(f"Error processing {file}: {e}")
                continue

    twitter_df_result.to_csv('D:/Research_PostGraduate/web3/tweet/outputs/onchain_time_range_all_nor.csv', index=False)

    total_count = cumulative_frequency_data.sum()
    percentage_cumulative_frequency_data = (cumulative_frequency_data / total_count) * 100
    print("Percentage cumulative frequency data:", percentage_cumulative_frequency_data)

    fig, ax = plt.subplots(figsize=(12, 10))
    percentage_cumulative_frequency_data.plot(kind='bar', ax=ax)
    ax.set_title(f"Transaction Frequency for all nor memecoin")
    ax.set_xlabel("Time Range")
    ax.set_ylabel("Frequency")
    plt.savefig(f"D:/Research_PostGraduate/web3/tweet/outputs/img/total_trans_fre_nor.png")  # 保存为PNG文件
    print(big_name_list)
pool_data_base_on_chain_nor()

def clean_pool_data_base_on_twitter_no_rug():
    twitter_folder_dic = "D:/Research_PostGraduate/web3/tweet/outputs/social_data"
    twitter_df_result = pd.DataFrame(columns=['big_coin_name', 'start_time', 'end_time'])
    cumulative_frequency_data = pd.Series()

    for file in tqdm(os.listdir(twitter_folder_dic), desc="Processing twitter"):
        if file.endswith(".csv"):
            coin_name = os.path.splitext(file)[0]
            parts = coin_name.split("_")
            if parts[-1] in ["ID","filter"]:
                continue
            first_part = parts[0]
            big_coin_name = first_part[1:]
            print(big_coin_name)
            file_path = os.path.join(twitter_folder_dic, file)
            twi_df = pd.read_csv(file_path, encoding='ISO-8859-1')
            twi_df['Timestamp'] = pd.to_datetime(twi_df['Timestamp'])
            start_time = twi_df['Timestamp'].min()
            end_time = twi_df['Timestamp'].max()


            if big_coin_name in ['$BABYBITCOIN', '2.0PEPE', 'ASPC', 'ASUKA', 'AWOKE', 'BASED', 'BEAST', 'BEE', 'BLADESOFGLORY', 'BTCPEP', 'BUBS', 'CAPT', 'CAT.AI', 'CUJO', 'DOGIRA', 'DOOM', 'DRF', 'DROPS', 'DYOR', 'EGG', 'ELONIUM', 'KENNY', 'PEPITO']:
                continue
            try:
                data_to_append = {'big_coin_name': big_coin_name, 'start_time': start_time, 'end_time': end_time}
                df_to_append = pd.DataFrame([data_to_append])
                twitter_df_result = pd.concat([twitter_df_result, df_to_append], ignore_index=True)

                time_range = pd.date_range(start=start_time, end=end_time, periods=21)
                twi_df['TimeRange'] = pd.cut(twi_df['Timestamp'], bins=time_range)
                frequency_data = twi_df['TimeRange'].value_counts().sort_index()

                new_index = pd.Series()
                for i, interval in enumerate(frequency_data.index):
                    new_interval = pd.Interval(left=i*5, right=(i+1)*5, closed='right')
                    new_index.at[new_interval] = frequency_data[i]

                frequency_data.index = new_index.index

                total_count = frequency_data.sum()
                percentage_data = (frequency_data / total_count) * 100
                weighted_frequency_data = percentage_data * total_count
                cumulative_frequency_data = cumulative_frequency_data.add(weighted_frequency_data, fill_value=0)
                
            except Exception as e:
                print(f"Error processing {file}: {e}")
                continue

    twitter_df_result.to_csv('D:/Research_PostGraduate/web3/tweet/outputs/twitter_time_range_all.csv', index=False)

    total_count = cumulative_frequency_data.sum()
    percentage_cumulative_frequency_data = (cumulative_frequency_data / total_count) * 100

    fig, ax = plt.subplots(figsize=(12, 10))
    percentage_cumulative_frequency_data.plot(kind='bar', ax=ax)
    ax.set_title(f"Tweet Frequency for all normal memecoin")
    ax.set_xlabel("Time Range")
    ax.set_ylabel("Frequency")
    plt.savefig(f"D:/Research_PostGraduate/web3/tweet/outputs/img/total_twi_fre_no_rug.png")  # 保存为PNG文件
    
# clean_pool_data_base_on_twitter_no_rug()


def move_file_on_chain():
    from_dictionary = "D:/Research_PostGraduate/web3/tweet/alldata/preparing_data"
    to_dictionary = "D:/Research_PostGraduate/web3/tweet/alldata/0_rugpull_confirm"
    check_dictionary = "D:/Research_PostGraduate/web3/tweet/alldata/0_rugpull_pool_confirm"
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    # Name,Market,Chain,Address,Social,ID,WarningText,Rugpull_level,WarningText_trans,address_code,Rugpull_comfirm,price_exist
    eth_df = pd.read_csv(eth_dic)

    for filename in os.listdir(check_dictionary):
        if filename.endswith(".csv"):
            coin_name = os.path.splitext(filename)[0]
            coin_name = coin_name[:-5]
            print("name: ",coin_name)
            csv_string = coin_name+".csv"
            # if coin_name.endswith("_clean"):
            ori_path = os.path.join(from_dictionary, csv_string)  
            save_path = os.path.join(to_dictionary, csv_string)  
            try:
                shutil.copy(ori_path, save_path)
            except:
                print(ori_path)

# move_file_on_chain()
