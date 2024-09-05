import pandas as pd
import os

def coinmarkey_cap_page_merge():
    merged_df = pd.DataFrame()
    current_dir = os.getcwd()
    # 遍历文件夹下所有的csv文件
    folder_path = 'outputs/sec_scrape'
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv") and file_name.startswith("coinmarketcap_page"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, encoding='latin-1')
            merged_df = pd.concat([merged_df, df])

    # 新增一列web_name
    merged_df['web_name'] = merged_df['Link'].apply(lambda x: x.split('/')[-2])

    # 将合并后的数据保存为新的csv文件
    merged_file_path = 'outputs/sec_scrape/coinmarketcap_page_merge.csv'  # 请将your_merged_file_path替换为你想要保存的文件路径
    merged_df.to_csv(merged_file_path, index=False)

# coinmarkey_cap_page_merge()

def coinmarkey_cap_page_detail_merge():
    merged_df = pd.DataFrame()
    current_dir = os.getcwd()
    for file_name in os.listdir(current_dir):
        if file_name.endswith(".csv") and file_name.startswith("coinmarketcap"):
            file_path = os.path.join(current_dir, file_name)
            df = pd.read_csv(file_path, encoding='latin-1')
            merged_df = pd.concat([merged_df, df])
    filtered_df = merged_df[~merged_df['Chain'].apply(lambda x: isinstance(x, float))]
    merged_df = filtered_df
    merged_df['chain_name'] = merged_df['Chain'].apply(lambda x: x.split(':')[0])

    # 将合并后的数据保存为新的csv文件
    merged_file_path = 'outputs/sec_scrape/coinmarketcap_detail.csv'  # 请将your_merged_file_path替换为你想要保存的文件路径
    merged_df.to_csv(merged_file_path, index=False)
# coinmarkey_cap_page_detail_merge()

def clean_duplicate():
    df = pd.read_csv("outputs/sec_scrape/coinmarketcap_detail.csv", encoding='latin-1')
    df.drop_duplicates()
    df.to_csv("outputs/sec_scrape/coinmarketcap_detail.csv", index=False)
clean_duplicate()