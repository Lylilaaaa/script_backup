from requests import Session
import json
from datetime import datetime, timedelta
from tqdm import tqdm
import os
import pandas as pd
import shutil
import matplotlib.pyplot as plt
def getInfo (chain_id,contract_address,from_timestamp,end_timestamp): # string,string,int,int
    url = "https://api.chainbase.online/v1/token/price/history" 
    api = '2fEjH1ab5Qc2iUfd3g4wHmSjkNJ' 
    parameters = { 'chain_id': chain_id, 'contract_address': contract_address,'from_timestamp':from_timestamp,'end_timestamp':end_timestamp} 
    # parameters = { 'chain_id': "1", 'contract_address': "0xcf0c122c6b73ff809c693db761e7baebe62b6a2e",'from_timestamp':1686134855,'end_timestamp':1686573359} 
    headers = {"accept": "application/json",'x-api-key': api}
    session = Session()
    session.headers.update(headers) 
    response = session.get(url, params=parameters) 
    info = json.loads(response.text)
    return info

def timestamp_convert(timestamp):
    real_time = datetime.utcfromtimestamp(timestamp)
    return real_time

def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)
        file.write('\n')

def get_price_chainbase(nor_rg):
    directory = f"D:/Research_PostGraduate/web3/tweet/alldata/{nor_rg}_data"
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    save_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/price_api_{nor_rg}"
    eth_df = pd.read_csv(eth_dic)
    for filename in tqdm(os.listdir(directory), desc="Processing unique topics"):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            coin_name = os.path.splitext(filename)[0]
            df = pd.read_csv(file_path)
            start_timestamp = int(df['timestamp'].iloc[0])
            start_datetime = timestamp_convert(start_timestamp)
            end_datetime = start_datetime + timedelta(days=29)
            end_timestamp = int(end_datetime.timestamp())

            address_code = eth_df[eth_df["Name"] == coin_name]["Address"].iloc[0]
            address_code = str(str(address_code).split("/")[-1])
            address_code = str(address_code.replace(" ", ""))
            save_path = os.path.join(save_dic, f"{coin_name}_price.json")
            result=getInfo("1",address_code,start_timestamp,end_timestamp)
            save_to_json(result,save_path)
            
# get_price_chainbase("preparing")

def price_exist(nor_rg):
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    save_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/price_api_{nor_rg}"
    eth_df = pd.read_csv(eth_dic)
    for filename in tqdm(os.listdir(save_dic), desc="Processing unique topics"):
        if filename.endswith(".json"):
            file_path = os.path.join(save_dic, filename)
            coin_name = os.path.splitext(filename)[0][:-6]

            with open(file_path, "r") as f:
                data = json.load(f)
            if data.get("data") is None or (data.get("code") == 429 and data.get("message") == "RequestLimitExceeded"):
                price_exist = 0
            else:
                price_exist = 1

            eth_df.loc[eth_df["Name"] == coin_name, "price_exist"] = price_exist
    eth_df.to_csv(eth_dic, index=False)
# price_exist("preparing")

def remove_price_data(nor_rg):
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    ori_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/preparing_data"
    save_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/{nor_rg}_data_price"
    eth_df = pd.read_csv(eth_dic)
    for filename in tqdm(os.listdir(ori_dic), desc="Processing unique topics"):
        if filename.endswith(".csv"):
            print(filename)
            coin_name = os.path.splitext(filename)[0]
            save_path = os.path.join(save_dic, filename)
            ori_path = os.path.join(ori_dic, filename)
            price_exist = eth_df.loc[eth_df["Name"] == coin_name,"price_exist"]
            print(price_exist)
            if int(price_exist.iloc[0]) == 1:
                shutil.move(ori_path, save_path)
# remove_price_data("nor")

def remove_price_data_json(nor_rg):
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    ori_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/price_api_preparing"
    save_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/{nor_rg}_data_price"
    eth_df = pd.read_csv(eth_dic)
    for filename in tqdm(os.listdir(ori_dic), desc="Processing unique topics"):
        if filename.endswith(".json"):
            coin_name = os.path.splitext(filename)[0][:-6]
            save_path = os.path.join(save_dic, filename)
            ori_path = os.path.join(ori_dic, filename)
            price_exist = eth_df.loc[eth_df["Name"] == coin_name,"price_exist"]
            if int(price_exist.iloc[0]) == 1:
                shutil.move(ori_path, save_path)
# remove_price_data_json("nor")

def price_drop_90(data_list):
    df = pd.DataFrame(data_list)
    df["updated_at"] = pd.to_datetime(df["updated_at"])
    df = df.sort_values("updated_at")
    highest_price = df["price"].max()
    day_30_price = df.iloc[-1]["price"]
    if highest_price == 0:
        return "First Day 0"
    price_drop_pct = (day_30_price - highest_price) / highest_price * 100
    
    if price_drop_pct < -95:
        return f"True_{price_drop_pct}%"
    else:
        return f"False_{price_drop_pct}%"


def price_plot():
    save_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/nor_data_price"  
    all_files = []
    eth_csv_path = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    eth_df =pd.read_csv(eth_csv_path)
    for root, dirs, files in os.walk(save_dic):
        for file in files:
            if file.endswith(".json"):
                print(os.path.join(root, file))
                all_files.append(os.path.join(root, file))
    for file_path in tqdm(all_files, desc="Processing unique topics"):
        coin_name = os.path.splitext(os.path.basename(file_path))[0][:-6]
        save_path = os.path.join(os.path.dirname(file_path), f"{coin_name}_price_plot.png")
        print(save_path)
        with open(file_path, 'r') as file:
            json_content = file.read()
            data_dict = json.loads(json_content)
            data_list = data_dict["data"]
            # "price": 4e-08, "symbol": "akita", "decimals": 18, "updated_at": "2021-02-28T22:00:00Z"
            is_90_persentage = price_drop_90(data_list)
            split_parts = is_90_persentage.split("_")
            df = pd.DataFrame(data_list)
            df["updated_at"] = pd.to_datetime(df["updated_at"])
            df = df.set_index("updated_at")
            plt.figure(figsize=(10, 6))
            plt.plot(df.index, df["price"])
            plt.xlabel('Time')
            plt.ylabel('Price')
            plt.title(f'Price over Time {is_90_persentage}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(save_path)
            eth_df.loc[eth_df["Name"] == coin_name, "price_drop"] = split_parts[-1]
    eth_df.to_csv(eth_csv_path, index=False)
# price_plot()


def price_rug_combine():
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    # Name,Market,Chain,Address,Social,ID,WarningText,Rugpull_level,WarningText_trans,address_code,Rugpull_comfirm,price_exist
    eth_df = pd.read_csv(eth_dic)
    save_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/nor_data_price"
    for filename in tqdm(os.listdir(save_dic), desc="Processing unique topics"):
        if filename.endswith(".json"):
            coin_name = os.path.splitext(filename)[0][:-6]
            rug_pull_warning = eth_df.loc[eth_df["Name"] == coin_name,"Rugpull_level"].values[0]
            rug_pull_comfirm = eth_df.loc[eth_df["Name"] == coin_name,"Rugpull_comfirm"].values[0]
            print(f"Coin: {coin_name}, rug pull warning: {rug_pull_warning}, rug pull comfirm: {rug_pull_comfirm}")
            print("\n")
# price_rug_combine()


def price_rug_combine():
    label_list_path = "D:/Research_PostGraduate/web3/tweet/alldata/labeled_list.csv"
    # token_address,pool_address,label,type
    label_list_df = pd.read_csv(label_list_path)
    label_list_df.columns = label_list_df.columns.str.lower()  # 将列名转换为小写

    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    # Name,Market,Chain,Address,Social,ID,WarningText,Rugpull_level,WarningText_trans,address_code,Rugpull_comfirm,price_exist
    eth_df = pd.read_csv(eth_dic)
    eth_df.columns = eth_df.columns.str.lower()  # 将列名转换为小写

    # 筛选label为0的token_address
    filtered_labels = label_list_df[label_list_df['label'] == 0]['token_address'].str.lower()
    print(filtered_labels)

    # 将两个 DataFrame 根据 address_code 进行合并
    merged_df = pd.merge(eth_df, filtered_labels, left_on='address_code', right_on='token_address', how='inner')
    print(eth_df['address_code'])

    # 输出匹配的内容
    print(merged_df[['token_address', 'address']])

# price_rug_combine()

def trans_cut():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/nor_data_price"
    # eth_csv_path = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    # eth_df =pd.read_csv(eth_csv_path)
    selected_events = ['Withdrawal', 'Swap', 'Transfer']
    for root, dirs, files in tqdm(os.walk(new_directory), desc="Processing unique topics"):
        for file in files:
            print(file)
            if file == "safereum_All_graph_coinmarketcap.csv":
                print("PASS")
                continue
            if file.endswith(".csv"):
                coin_name = os.path.splitext(file)[0]
                if coin_name.endswith("_clean"):
                    print("PASS")
                    continue
            if file.endswith(".csv"):
                coin_name = os.path.splitext(file)[0]
                new_path = os.path.join(root, f"{coin_name}_clean.csv")
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                print(f"处理前的行数: {len(df)}")
                df['date'] = pd.to_datetime(df['date'])
                df = df[df['event_txt'].str.split('(').str[0].isin(selected_events)]
                df = df[df['date'] <= df['date'].min() + timedelta(days=30)]
                print(f"处理后的行数: {len(df)}")
                df.to_csv(new_path, index=False)
# trans_cut()

def trans_cut_separate():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/nor_data_price"
    selected_events = ['Withdrawal', 'Swap', 'Transfer']
    file_list = os.listdir(new_directory)
    for file in tqdm(file_list, desc="Processing unique topics"):
        if file.endswith(".csv"):
            coin_name = os.path.splitext(file)[0]
            print(coin_name)
            new_path = os.path.join(new_directory, f"{coin_name}_clean.csv")
            file_path = os.path.join(new_directory, file)
            df = pd.read_csv(file_path)
            print(f"处理前的行数: {len(df)}")
            df['date'] = pd.to_datetime(df['date'])
            df = df[df['event_txt'].str.split('(').str[0].isin(selected_events)]
            df = df[df['date'] <= df['date'].min() + timedelta(days=30)]
            print(f"处理后的行数: {len(df)}")
            df.to_csv(new_path, index=False)
# trans_cut_separate()

def detele_clean():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/nor_data_price"
    selected_events = ['Withdrawal', 'Swap', 'Transfer']
    file_list = os.listdir(new_directory)
    for file in tqdm(file_list, desc="Processing unique topics"):
        if file.endswith(".csv"):
            coin_name = os.path.splitext(file)[0]
            if coin_name.endswith("_clean"):
                os.remove(os.path.join(new_directory, file))
                print(f"Deleted {file}")
                continue  # 继续处理下一个文件
# detele_clean()



