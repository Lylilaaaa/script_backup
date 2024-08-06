import pandas as pd
from tqdm import tqdm
import os
def get_merge():
    # 读取包含数据的CSV文件
    df = pd.read_csv('outputs\Pepe_merged_file.csv')

    # 创建一个空的DataFrame来存储拆分后的数据
    new_df = pd.DataFrame(columns=['src', 'dst','time'])
    dfs = []
    # 遍历每一行，将字符串拆分后放入新的DataFrame
    for index, row in df.iterrows():
        time = row['Timestamp']
        retweets_string = row['Retweets IDs']
        if isinstance(retweets_string, str):
            retweets_list = retweets_string.split(',')
            user_name = row['UserName']
            data = [{'src': user_name, 'dst': dst,'time': time} for dst in retweets_list]
            dfs.append(pd.DataFrame(data))
    new_df = pd.concat(dfs, ignore_index=True)
    # 将新的DataFrame保存为CSV文件
    new_df.to_csv('outputs\Pepe_edge.csv', index=False)
def get_merge_onchain():
    # 读取包含数据的CSV文件
    new_df = pd.DataFrame(columns=['src', 'dst', 'time'])
    dfs = []
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/rg_data"
    for filename in tqdm(os.listdir(new_directory), desc="Processing unique topics"):
        dfs = []
        if filename.endswith(".csv"):
            file_path = os.path.join(new_directory, filename)
            coin_name = os.path.splitext(filename)[0]
            df = pd.read_csv(file_path)
            for index, row in df.iterrows():
                time = row['timestamp']
                from_ = row['topic1']
                to_ = row['topic2']
                data = {'src': from_, 'dst': to_, 'time': time}
                dfs.append(data)
    
        merged_df = pd.DataFrame(dfs)
        merged_df.to_csv(f'D:/Research_PostGraduate/web3/tweet/alldata/rg_edge/{coin_name}.csv', index=False)
get_merge_onchain()