import pandas as pd
from requests import Session
import json
from tqdm import tqdm
import os

def getSolFromMerge():
    path = "D:/Research_PostGraduate/web3/tweet/outputs/sec_scrape"
    file_path = os.path.join(path, "coinmarketcap_detail.csv")
    df = pd.read_csv(file_path)
    sol_df = df[df['chain_name'] == 'Solana']
    sol_file_path = 'D:/Research_PostGraduate/web3/tweet/outputs/sec_scrape/coinmarketcap_detail_sol.csv'  # 请将your_merged_file_path替换为你想要保存的文件路径
    sol_df.to_csv(sol_file_path, index=False)
# getSolFromMerge()

def getInfo(address):
    url = f"https://api.rugcheck.xyz/v1/tokens/{address}/report"
    headers = {"accept": "application/json"}
    session = Session()
    session.headers.update(headers)
    response = session.get(url)
    if response.ok:  # 检查请求是否成功
        if response.text:  # 检查响应内容是否为空
            info = json.loads(response.text)
            return info
        else:
            print(f"Empty response for address: {address}")
            return None
    else:
        print(f"Request failed for address: {address}")
        return None

def read_report_summary():
    df = pd.read_csv('D:/Research_PostGraduate/web3/tweet/outputs/sec_scrape/coinmarketcap_detail_sol.csv', encoding='latin-1')
    df['Address'] = df['Address'].str.split('/', expand=True)[4]
    # Open the output file in append mode
    with open('D:/Research_PostGraduate/web3/tweet/outputs/sec_scrape/coinmarketcap_detail_Sol_risk_report_sum.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Write the header row
        csvfile.write('Address,score,risks\n')

        # Iterate over the DataFrame with tqdm to display the progress bar
        for address in tqdm(df['Address'], desc="Processing"):
            info = getInfo(address)
           
            if info:
                try:
                    risk_score = info["score"]
                    risk_string = ""
                    for risk in info["risks"]:
                        risk_name = risk["name"]
                        risk_value = risk["value"]
                        risk_description = risk["description"]
                        risk_score = risk["score"]
                        risk_level = risk["level"]
                        risk_string += f"name:{risk_name};value:{risk_value};description:{risk_description};score:{risk_score};level:{risk_level}/"
                    csvfile.write(f"{address},{risk_score},{risk_string}\n")
                except KeyError as e:
                    print(f"KeyError for address {address}: {e}")
            else:
                print(f"No info for address {address}")
read_report_summary()

# def rank_risk():
#     df = pd.read_csv('D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Solana_risk.csv', encoding='latin-1')
#     df = df[df.iloc[:, 2] != '[]']
#     df = df.dropna()
#     df.to_csv('D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Solana_risk_processed.csv', index=False, encoding='utf-8')

# rank_risk()
