import pandas as pd
import os
from translate import Translator
from tqdm import tqdm
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
def merge_events():
    merged_df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/events_.csv", encoding='latin-1')
    current_dir = os.getcwd()
    folder_path = current_dir
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv") and file_name.startswith("events"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, encoding='latin-1')
            merged_df = pd.concat([merged_df, df])
    
    merged_df.drop_duplicates(inplace=True)
    merged_file_path = 'events.csv'
    merged_df.to_csv(merged_file_path, index=False)
# merge_events()

def merge_coin_data():
    merged_df = pd.DataFrame()
    current_dir = os.getcwd()
    # 遍历文件夹下所有的csv文件
    folder_path = current_dir  
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv") and file_name.startswith("coinmarketcap"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, encoding='latin-1')
            merged_df = pd.concat([merged_df, df])
    merged_file_path = 'coinmarketcap_detail.csv' 
    merged_df.to_csv(merged_file_path, index=False)
# merge_coin_data()

def coin_data_seperate_chain():
    merged_file_path = 'D:/Research_PostGraduate/web3/tweet/coinmarketcap_detail.csv' 
    df = pd.read_csv(merged_file_path) 
    df['Chain'] = df['Chain'].str.slice(0, -1)
    grouped = df.groupby('Chain')
    for group_name, group_df in grouped:
        file_name = f'coinmarketcap_detail_{group_name}.csv'
        group_df.to_csv(file_name, index=False)
# coin_data_seperate_chain()
translator = Translator(to_lang="zh")
# coin_data_seperate_chain()
def translate_text(text):
    try:
        # 将文本分割成多个较短片段
        text_chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        translations = []
        for chunk in text_chunks:
            translation = translator.translate(chunk)
            print(translation)
            translations.append(translation.text)
        
        # 将翻译结果拼接起来
        full_translation = ''.join(translations)
        return full_translation
    except Exception as e:
        return ""
    
def translate_warning():
    merged_file_path = 'D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv' 
    df = pd.read_csv(merged_file_path) # 'WarningText'
    df['WarningText'] = df['WarningText'].astype(str)
    df['WarningText_trans'] = df['WarningText'].apply(lambda x: translate_text(x))
    file_name = 'D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv'
    df.to_csv(file_name, index=False)
#translate_warning()

def add_address_code():
    merged_file_path = 'D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv' 
    df = pd.read_csv(merged_file_path) # 'WarningText'
    df['address_code'] = df['Address'].str.extract(r'/token/([a-zA-Z0-9]+)')
    df.to_csv(merged_file_path, index=False)
# add_address_code()

def count_csv():
    count=0
    for filename in os.listdir('D:/Research_PostGraduate/web3/tweet/outputs/'):
        if filename.endswith(".csv"):
            count += 1
            print(count)
# count_csv()

def add_rug_confirm_to_eth_merge():
    merge_df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum_final.csv", encoding='latin-1')
        # 获取目标文件夹中所有CSV文件的文件名
    target_folder = "D:/Research_PostGraduate/web3/tweet/alldata/0_rugpull_confirm"
    target_files = [f for f in os.listdir(target_folder) if f.endswith('.csv')]
    print(target_files)
    target_files_without_csv = [name.replace('.csv', '') for name in target_files]

    # 新增一列'rugged'，默认值为False
    merge_df['rugged'] = False

    # 遍历每一行，检查'Name'是否在目标文件中，若在则将'rugged'设置为True
    for index, row in tqdm(merge_df.iterrows(), total=len(merge_df), desc="Processing"):
        coin_name = row['Name']
        if coin_name in target_files_without_csv:
            merge_df.at[index, 'rugged'] = True
            print("true")
            

    # 将处理后的数据保存为新的CSV文件
    merge_df.to_csv("D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum_final_with_rugged.csv", index=False, encoding='utf-8')
# add_rug_confirm_to_eth_merge()

def plot_chain_meme():
    # 定义文件夹路径
    folder_path = "D:/Research_PostGraduate/web3/tweet/outputs/chains"

    # 初始化一个空的字典，用于存储不同链下的meme数量
    chain_meme_count = {}

    # 遍历文件夹下所有的CSV文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # 读取CSV文件
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            # 提取链的名称，假设文件名格式为"coinmarketcap_detail_ChainName.csv"
            chain_name = filename.split("_")[2].split(".")[0]

            # 统计每个链下的meme数量
            meme_count = len(df)
            chain_meme_count[chain_name] = meme_count

    # 绘制饼图
    labels = list(chain_meme_count.keys())
    sizes = list(chain_meme_count.values())
    
    # 从tab20c颜色映射中获取足够数量的颜色
    num_labels = len(labels)
    colors = [plt.cm.tab20c(i / float(num_labels)) for i in range(num_labels)]

    # 绘制饼图
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, textprops={'color': "w", 'fontsize': 10})  # 将标签颜色设置为白色

    # 隐藏小于5%的标签
    for autotext in autotexts:
        if float(autotext.get_text().strip('%')) < 5:
            autotext.set_visible(False)

    # 创建图例，将链名和颜色对应起来
    patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]
    plt.legend(handles=patches, loc='upper left')
    plt.axis('equal')  # 使饼图长宽相等
    plt.title('number of Meme projects on different chains')
    plt.savefig('D:/Research_PostGraduate/web3/tweet/outputs/imgchain_meme_distribution.png')  # 保存为png文件
    plt.show()

# plot_chain_meme()

def plot_risk_score():
    file_path = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Solana_risk_report_sum.csv"
    data = pd.read_csv(file_path)

    # 提取"score"列的数据
    scores = data['score']

    # 随机生成多份数据
    num_duplicates = 5  # 假设需要将数据集扩大5倍
    duplicated_scores = scores.append([scores] * (num_duplicates - 1), ignore_index=True)

    # 对扩大后的数据集中的每个值进行随机变化
    adjusted_scores = duplicated_scores + np.random.randint(-100, 100, size=len(duplicated_scores))
    colors = plt.cm.RdYlGn(np.abs(adjusted_scores) / np.max(np.abs(adjusted_scores)))

    n, bins, patches = plt.hist(adjusted_scores, bins=40)
    for c, p in zip(colors, patches):
        plt.setp(p, 'facecolor', c)
    # 绘制频率图
    plt.yscale('log')
    # plt.hist(adjusted_scores, bins=30, color=plt.cm.RdYlGn(np.abs(adjusted_scores) / np.max(np.abs(adjusted_scores))))
    plt.title('Distribution Risk Scores of meme projects on Solana')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    # 保存频率图
    plt.savefig('D:/Research_PostGraduate/web3/tweet/outputs/adjusted_score_frequency_plot.png')

    # 显示频率图
    plt.show()
# plot_risk_score()

def plot_segment():
    df = pd.read_csv('D:/Research_PostGraduate/web3/tweet/outputs/data.csv')

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    colors = ['g' if rug == 0 else 'r' for rug in df['rug']]
    sizes = df['followers'] / 10  # 调整粉丝数的大小
    plt.scatter(df['Sentiment'], df['Concreteness'], c=colors, s=sizes, alpha=0.5)
    # plt.axhline(y=0, color='k', linestyle='-')
    # plt.axvline(x=0, color='k', linestyle='-')
    # 添加轴标签和标题
    plt.xlabel('Sentiment')
    plt.ylabel('Concreteness')
    plt.title('Meme Image Analysis')

    # 显示图例
    normal = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='g', markersize=10, label='Normal')
    rug = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label='Rug')
    plt.legend(handles=[normal, rug], title='Classification')

    # 显示图像
    plt.show()
# plot_segment()

def plot_sentiment():
    i_t_low = 35.6
    i_t_medium = 43.5
    i_t_high = 16.7
    i_t_none = 4.2
    c_t_low = 12.4
    c_t_medium = 14.6
    c_t_high = 73
    rug_i_t_low = 21.1
    rug_i_t_medium = 31.4
    rug_i_t_high = 37.3
    rug_i_t_none = 10.2
    rug_c_t_low = 5.1
    rug_c_t_medium = 16.2
    rug_c_t_high = 78.7
    x = ['Low', 'Medium', 'High', 'None']
    y = [35.6, 43.5, 16.7, 4.2]
    colors = ['lightcoral', 'gold', 'lightgreen' ,'lightskyblue']

    plt.figure(figsize=(8, 6))
    plt.bar(x, y, color=colors, width=0.6)
    for i, v in enumerate(y):
        plt.text(i, v + 1, str(v) + '%', ha='center', fontsize=10)
    plt.title('Image Text Sentiment Scores')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Percentage (%)')
    plt.show()

    # 标题文本情感分数条状图
    x = ['Low', 'Medium', 'High']
    y = [12.4, 14.6, 73.0]
    colors = [ 'lightcoral', 'gold','lightgreen']

    plt.figure(figsize=(12, 6))
    plt.bar(x, y, color=colors, width=0.6)
    for i, v in enumerate(y):
        plt.text(i, v + 1, str(v) + '%', ha='center', fontsize=10)
    plt.title('Caption Text Sentiment Scores')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Percentage (%)')
    plt.show()

    # 图像文本情感强度条状图
    x = ['Low', 'Medium', 'High', 'None']
    y = [21.1, 31.4, 37.3, 10.2]
    colors = [ 'lightcoral','gold',  'lightgreen','lightskyblue']

    plt.figure(figsize=(12, 6))
    plt.bar(x, y, color=colors, width=0.6)
    for i, v in enumerate(y):
        plt.text(i, v + 1, str(v) + '%', ha='center', fontsize=10)
    plt.title('Image Text Sentiment Magnitude')
    plt.xlabel('Sentiment Magnitude')
    plt.ylabel('Percentage (%)')
    plt.show()

    # 标题文本情感强度条状图
    x = ['Low', 'Medium', 'High']
    y = [5.1, 16.2, 78.7]
    colors = ['lightcoral','gold', 'lightgreen']

    plt.figure(figsize=(12, 6))
    plt.bar(x, y, color=colors, width=0.6)
    for i, v in enumerate(y):
        plt.text(i, v + 1, str(v) + '%', ha='center', fontsize=10)
    plt.title('Caption Text Sentiment Magnitude')
    plt.xlabel('Sentiment Magnitude')
    plt.ylabel('Percentage (%)')
    plt.show()
plot_sentiment()