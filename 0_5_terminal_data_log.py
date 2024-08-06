import pandas as pd

# 读取CSV文件
merged_df = pd.read_csv('D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum_final.csv', encoding='latin-1')
#29-xx
# 生成命令
# .iloc[10:20]
#-1:-91
# .head(10)
# selected_rows = merged_df[merged_df['Rugpull_level'] == 1].head(30)
# for index, row in merged_df.iloc[19:29].iterrows():
commands = []
# for index, row in selected_rows.iterrows():
#     command = f"chifra export --fmt csv --logs {row['address_code']} > {row['Name']}.csv"
#     commands.append(command)
#     print(f"https://coinmarketcap.com/currencies/{row['Name']}")#     print("\n")
rugpull_meme_df = merged_df[merged_df['Rugpull_comfirm'] == 0]
print(len(rugpull_meme_df))
random_rows = rugpull_meme_df.sample(n=90, random_state=1)
print(random_rows)
for index, row in random_rows.iterrows():
    command = f"chifra export --fmt csv --logs {row['address_code']} > {row['Name']}_pool.csv"
    commands.append(command)

full_command = " && ".join(commands)

print(full_command)