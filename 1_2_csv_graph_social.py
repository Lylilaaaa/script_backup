import pandas as pd

# # 读取两个表格
# df1 = pd.read_csv('outputs\$Pepe_2023-04-14_2023-04-20.csv')
# df2 = pd.read_csv('outputs\Pepe_retweets_ID.csv')
# df1.drop('Retweets IDs', axis=1, inplace=True)
# # 按照 "Tweet URL" 列合并两个表格
# result = pd.merge(df1, df2, on='Tweet URL', how='outer')

# for index, row in result.iterrows():
#     retweets_string = row['Retweets IDs']
#     if isinstance(retweets_string,str):
#         retweets_list = retweets_string.split(',')
#         unique_retweets_set = set(retweets_list)
#         unique_retweets_string = ','.join(unique_retweets_set)
#         result.loc[index, 'Retweets IDs'] = unique_retweets_string
#         result.loc[index, 'Unique Retweets Count'] = len(unique_retweets_set)

# # 将合并的结果保存到新的文件中
# result.to_csv('outputs\Pepe_merged_file.csv', index=False)

# def plot_twitter_content():
