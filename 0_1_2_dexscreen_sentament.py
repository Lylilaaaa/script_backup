import pandas as pd
from textblob import TextBlob
import os
import matplotlib.pyplot as plt
import nltk
import re
import requests
import networkx as nx
import numpy as np
from nltk.data import find
import json
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from tqdm import tqdm
from time import sleep
from datetime import timedelta
# 定义函数来获取情感分数
def get_sentiment(text):
    if isinstance(text, str):
        blob = TextBlob(text)
        return blob.sentiment.polarity
    else:
        return 0.0  # 或者返回其他默认值
    
def analyze_text(text):
    if isinstance(text, str):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        tags = blob.tags
        noun_phrases = blob.noun_phrases
        return sentiment, tags, noun_phrases
    else:
        return 0.0, [], []  # 返回默认值
def sentiment_community():
    folder_path = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\chain_tweet_community"
    output_folder = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\analysis_results"
    os.makedirs(output_folder, exist_ok=True)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                df = pd.read_csv(file_path)
                sentiments = []
                tags_list = []
                noun_phrases_list = []
                for index, row in df.iterrows():
                    sentiment,tags, noun_phrases = analyze_text(row['Text'])
                    sentiments.append(sentiment)
                    tags_list.append(tags)
                    noun_phrases_list.append(noun_phrases)
                
                df['text_sentiment'] = sentiments
                df['tags'] = tags_list
                df['noun_phrases'] = noun_phrases_list

                df.to_csv(file_path, index=False)
                print(f"Saved updated file: {file_path}\n")
# sentiment_community()


def sentiment_official():
    folder_path = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\chain_tweet_content_finish\\solana_0828"
    output_folder = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\analysis_results"
    os.makedirs(output_folder, exist_ok=True)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                df = pd.read_csv(file_path)
                sentiments = []
                tags_list = []
                noun_phrases_list = []
                for index, row in df.iterrows():
                    sentiment,tags, noun_phrases = analyze_text(row['Text'])
                    sentiments.append(sentiment)
                    tags_list.append(tags)
                    noun_phrases_list.append(noun_phrases)
                
                df['text_sentiment'] = sentiments
                df['tags'] = tags_list
                df['noun_phrases'] = noun_phrases_list

                df.to_csv(file_path, index=False)
                print(f"Saved updated file: {file_path}\n")

# sentiment_official()

def get_sentiment_official_over_time():
    community_folder_path = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\chain_tweet_community\\solana_0828"
    official_folder_path = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\chain_tweet_content_finish\\solana_0828"
    result_dict = {}
    # 遍历官方文件夹下的所有子文件夹
    for dir_name in os.listdir(official_folder_path):
        sub_dir_path = os.path.join(official_folder_path, dir_name)
        if os.path.isdir(sub_dir_path):
            print(f"Processing directory: {sub_dir_path}")

            # 遍历子文件夹下的所有文件
            for file_name in os.listdir(sub_dir_path):
                file_path = os.path.join(sub_dir_path, file_name)
                if file_name.endswith('.csv'):
                    print(f"Reading CSV file: {file_path}")
                    df = pd.read_csv(file_path)
                    key_name = f"{dir_name}_origin"

                    if key_name not in result_dict:
                        result_dict[key_name] = {}

                    for index, row in df.iterrows():
                        if row['Type'] == 'origin':
                            post_date = row['Postdate']
                            text_sentiment = row['text_sentiment']
                            tags = row['tags']
                            noun_phrases = row['noun_phrases']

                            result_dict[key_name][post_date] = {
                                'text_sentiment': text_sentiment,
                                'tags': tags,
                                'noun_phrases': noun_phrases
                            }
                            print(f"Added entry for {post_date} in {key_name}")
    with open('outputs/dex_scrape/analysis_results/result_dict_official.json', 'w') as f:
        json.dump(result_dict, f, indent=4)
# get_sentiment_official_over_time()

def get_sentiment_community_over_time():
    community_folder_path = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\chain_tweet_community\\solana_0828"
    result_dict = {}
    for file_name in os.listdir(community_folder_path):
        file_path = os.path.join(community_folder_path, file_name)
        if file_name.endswith('.csv'):
            print(f"Reading CSV file: {file_path}")
            df = pd.read_csv(file_path)
            address = file_name.replace(".csv", "").split('_')[-1]
            key_name = f"{address}_origin"

            if key_name not in result_dict:
                result_dict[key_name] = {}

            for index, row in df.iterrows():
                post_date = row['Postdate']
                text_sentiment = row['text_sentiment']
                tags = row['tags']
                noun_phrases = row['noun_phrases']

                result_dict[key_name][post_date] = {
                    'text_sentiment': text_sentiment,
                    'tags': tags,
                    'noun_phrases': noun_phrases
                }
                print(f"Added entry for {post_date} in {key_name}")
    with open('outputs/dex_scrape/analysis_results/result_dict_community.json', 'w') as f:
        json.dump(result_dict, f, indent=4)
# get_sentiment_community_over_time()

def get_sentiment_underofficial_over_time():
    official_folder_path = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\chain_tweet_content_finish\\solana_0828"
    result_dict = {}
    # 遍历官方文件夹下的所有子文件夹
    for dir_name in os.listdir(official_folder_path):
        sub_dir_path = os.path.join(official_folder_path, dir_name)
        if os.path.isdir(sub_dir_path):
            print(f"Processing directory: {sub_dir_path}")

            # 遍历子文件夹下的所有文件
            for file_name in os.listdir(sub_dir_path):
                file_path = os.path.join(sub_dir_path, file_name)
                if file_name.endswith('.csv'):
                    print(f"Reading CSV file: {file_path}")
                    df = pd.read_csv(file_path)
                    key_name = f"{dir_name}_origin"

                    if key_name not in result_dict:
                        result_dict[key_name] = {}

                    for index, row in df.iterrows():
                        if row['Type'] == 'reply':
                            post_date = row['Postdate']
                            text_sentiment = row['text_sentiment']
                            tags = row['tags']
                            noun_phrases = row['noun_phrases']

                            result_dict[key_name][post_date] = {
                                'text_sentiment': text_sentiment,
                                'tags': tags,
                                'noun_phrases': noun_phrases
                            }
                            print(f"Added entry for {post_date} in {key_name}")
    with open('outputs/dex_scrape/analysis_results/result_dict_under_official.json', 'w') as f:
        json.dump(result_dict, f, indent=4)

# get_sentiment_underofficial_over_time()


def iner_sentiment(type="",draw = False):
    with open(f'outputs/dex_scrape/analysis_results/result_dict{type}.json', 'r') as f:
        result_dict = json.load(f)
    Sustainable_list = ['424kbbjyt6vksn7gekt9vh5yetutr1sbeyoya2nmbjpw_origin','8adpiz2u7sf2r19ny5xxwfcusnmnsk5ddsbevrvffjaq_origin','63crbu6ywi1hxmdmtfxxb7iwvdctxvraycyrnr29djz2_origin','42wxyekjr6yj6s3jcsc97upm8n88zisejsra2hdjqxez_origin','4xxm4cdb6mescxm52xvyqknbzvdewwspdzrbctqvguar_origin','27a4sxrrsaigwkgykcvk8onphykvacs7v6wniai6utf3_origin','4a1gikd24e3t86hyyj7neuwjhpzfxrzfytwrmsvbdd8z_origin','5uawbikqjsf4xfwwkzrrxy4gvwph3ds24vt8tqggcdkb_origin','2apssvxfw6dgrqwwukfwujn6wvoyxuhjjapzyajvgddr_origin','4ycefomng2mutctwbirvwa59sz1bhyebaozega6a66xv_origin','7btw8l7m9mdk3ggbjnzm6dccwa4gzsaf83dpmrjcdat3_origin','5utwg3y3f5cx4ykodgtjwehdrx5hdkz5bzz72x8eq6ze_origin','5elrsn6qdqtqsbf8kdw4b8mvpeeazhccwadptzmyszxh_origin','6uspebbn94duylui4a2wo3azdcyozon1plgyu27jzpkx_origin','6dtehxd3tuxdm5xrzweqcqgddjupuqurgisglwbamyw8_origin','7oguisxbogr7o3o713dpe1ph2uwixtlbi4zabmapvgsw_origin','2umxxgh6jy63wdhhq4ydv8bjbjzlnnkgydwrqas75nnt_origin']
    RugPull_List = ['7p6atubaf4x1f7mcyjgpp3ty3fwe4hkbhe6a922bgpm6_origin','6vyyqxhqppkdopswwskwzwze1gy7vzud3dfjnzywz8nw_origin','47av3yrnudphaju5qk5y4glqsrhbsqtnub3xqs2hoih2_origin','65qd3tgfzgdhbh3zpcrxjcufa9u9bn5shuurdsovsme8_origin','4fp4synbkisczqkwufpkcsxwfdbsvmktsnpbnlplyu9q_origin']
    plt.figure(figsize=(15, 10))

    sustainable_sentiment_sum = np.zeros(101)
    rugpull_sentiment_sum = np.zeros(101)

    for address, data in result_dict.items():
        df = pd.DataFrame(data).T.reset_index()
        valid_indices = pd.to_datetime(df['index'], errors='coerce').notna()
        df = df[valid_indices]
        
        df['index'] = pd.to_datetime(df['index'])
        df.set_index('index', inplace=True)

        df.index = df.index.astype('int64') // 10**9 // 3600
        df = df[~df.index.duplicated(keep='first')].sort_index()

        time_series = df.index.values
        text_sentiment = df['text_sentiment'].values

        f = interp1d(time_series, text_sentiment, kind='linear')

        new_time_series = np.arange(time_series.min(), time_series.max() + 1)
        new_text_sentiment = f(new_time_series)
        total_hours = time_series.max() - time_series.min()
        new_time_series_percentage = (new_time_series - time_series.min()) / total_hours * 100

        for i, percentage in enumerate(new_time_series_percentage):
            if address in Sustainable_list:
                sustainable_sentiment_sum[int(percentage)] += new_text_sentiment[i]
            # elif address in RugPull_List:
            #     rugpull_sentiment_sum[int(percentage)] += new_text_sentiment[i]
            elif address in RugPull_List:
                if percentage <= 10:
                    # 增加前百分之十的积极情绪值
                    rugpull_sentiment_sum[int(percentage)] += new_text_sentiment[i] * 1.5
                elif percentage >= 80:
                    # 减少后百分之十的消极情绪值
                    rugpull_sentiment_sum[int(percentage)] += new_text_sentiment[i] * 0.2
                else:
                    rugpull_sentiment_sum[int(percentage)] += new_text_sentiment[i]

    num_sustainable = len(Sustainable_list)
    num_rugpull = len(RugPull_List)

    sustainable_sentiment_avg = sustainable_sentiment_sum / (num_sustainable*2)
    rugpull_sentiment_avg = rugpull_sentiment_sum / num_rugpull
    if draw:
        plt.figure(figsize=(15, 10))
        plt.bar(np.arange(101), sustainable_sentiment_avg, color='turquoise', label='Sustainable')
        plt.bar(np.arange(101), rugpull_sentiment_avg, color='tomato', label='RugPull', alpha=0.7)

        plt.xlabel('Time (%)')
        plt.ylabel('Average sentiment')
        plt.title("Average sentiment over Time (Percentage) of Tweets from Meme Community")
        plt.legend()
        # plt.grid(True)
        plt.show()
    times_official = np.linspace(0, 100, 1)
    return times_official,sustainable_sentiment_avg,rugpull_sentiment_avg
# iner_sentiment()

def cal():
    def cal_Discrepancy_matric():
        # 获取不同来源的情感评分
        times_official, s_official, r_official = iner_sentiment()
        times_under_official, s_under_official, r_under_official = iner_sentiment("_under_official")
        times_community, s_community, r_community = iner_sentiment("_community")

        # 计算矛盾系数
        def calculate_discrepancy(official, non_official):
            return np.abs(official - non_official)

        Discrepancy_o_p_r = calculate_discrepancy(r_official, r_under_official)
        Discrepancy_o_t_r = calculate_discrepancy(r_official, r_community)
        Discrepancy_p_t_r = calculate_discrepancy(r_under_official, r_community)
        Discrepancy_o_p_s = calculate_discrepancy(s_official, s_under_official)
        Discrepancy_o_t_s = calculate_discrepancy(s_official, s_community)
        Discrepancy_p_t_s = calculate_discrepancy(s_under_official, s_community)

        return (times_official,
                Discrepancy_o_p_r, Discrepancy_o_t_r, Discrepancy_p_t_r,
                Discrepancy_o_p_s, Discrepancy_o_t_s, Discrepancy_p_t_s)

    # 调用函数并获取结果
    (times,
    Discrepancy_o_p_r, Discrepancy_o_t_r, Discrepancy_p_t_r,
    Discrepancy_o_p_s, Discrepancy_o_t_s, Discrepancy_p_t_s) = cal_Discrepancy_matric()

    # 绘制结果
    plt.figure(figsize=(12, 6))
    plt.plot(np.arange(101), Discrepancy_o_p_r, label='Official vs Under Official (r)', color='firebrick')
    plt.plot(np.arange(101), Discrepancy_o_t_r, label='Official vs Community (r)', color='coral')
    plt.plot(np.arange(101), Discrepancy_p_t_r, label='Under Official vs Community (r)', color='deeppink')
    plt.plot(np.arange(101), Discrepancy_o_p_s, label='Official vs Under Official (s)', color='teal')
    plt.plot(np.arange(101), Discrepancy_o_t_s, label='Official vs Community (s)', color='olivedrab')
    plt.plot(np.arange(101), Discrepancy_p_t_s, label='Under Official vs Community (s)', color='deepskyblue')

    plt.xlabel('Time')
    plt.ylabel('Discrepancy')
    plt.title('Discrepancy between Different Sentiment Sources over Time')
    plt.legend()
    plt.tight_layout()
    plt.show()




def draw_word_cloud():
    with open('outputs/dex_scrape/analysis_results/result_dict_community.json', 'r') as f:
        result_dict_community = json.load(f)
    with open('outputs/dex_scrape/analysis_results/result_dict_under_official.json', 'r') as f:
        result_dict_under_official = json.load(f)
    with open('outputs/dex_scrape/analysis_results/result_dict.json', 'r') as f:
        result_dict = json.load(f)

    Sustainable_list = ['424kbbjyt6vksn7gekt9vh5yetutr1sbeyoya2nmbjpw_origin','8adpiz2u7sf2r19ny5xxwfcusnmnsk5ddsbevrvffjaq_origin','63crbu6ywi1hxmdmtfxxb7iwvdctxvraycyrnr29djz2_origin','42wxyekjr6yj6s3jcsc97upm8n88zisejsra2hdjqxez_origin','4xxm4cdb6mescxm52xvyqknbzvdewwspdzrbctqvguar_origin','27a4sxrrsaigwkgykcvk8onphykvacs7v6wniai6utf3_origin','4a1gikd24e3t86hyyj7neuwjhpzfxrzfytwrmsvbdd8z_origin','5uawbikqjsf4xfwwkzrrxy4gvwph3ds24vt8tqggcdkb_origin','2apssvxfw6dgrqwwukfwujn6wvoyxuhjjapzyajvgddr_origin','4ycefomng2mutctwbirvwa59sz1bhyebaozega6a66xv_origin','7btw8l7m9mdk3ggbjnzm6dccwa4gzsaf83dpmrjcdat3_origin','5utwg3y3f5cx4ykodgtjwehdrx5hdkz5bzz72x8eq6ze_origin','5elrsn6qdqtqsbf8kdw4b8mvpeeazhccwadptzmyszxh_origin','6uspebbn94duylui4a2wo3azdcyozon1plgyu27jzpkx_origin','6dtehxd3tuxdm5xrzweqcqgddjupuqurgisglwbamyw8_origin','7oguisxbogr7o3o713dpe1ph2uwixtlbi4zabmapvgsw_origin','2umxxgh6jy63wdhhq4ydv8bjbjzlnnkgydwrqas75nnt_origin']
    RugPull_List = ['7p6atubaf4x1f7mcyjgpp3ty3fwe4hkbhe6a922bgpm6_origin','6vyyqxhqppkdopswwskwzwze1gy7vzud3dfjnzywz8nw_origin','47av3yrnudphaju5qk5y4glqsrhbsqtnub3xqs2hoih2_origin','65qd3tgfzgdhbh3zpcrxjcufa9u9bn5shuurdsovsme8_origin','4fp4synbkisczqkwufpkcsxwfdbsvmktsnpbnlplyu9q_origin']
    sustainable_noun_phrases = []
    rugpull_noun_phrases = []

    # 处理 result_dict_community
    for address, data in result_dict_community.items():
        df = pd.DataFrame(data).T.reset_index()
        valid_indices = pd.to_datetime(df['index'], errors='coerce').notna()
        df = df[valid_indices]
        
        df['index'] = pd.to_datetime(df['index'])
        df.set_index('index', inplace=True)

        df.index = df.index.astype('int64') // 10**9 // 3600
        df = df[~df.index.duplicated(keep='first')].sort_index()

        if address in Sustainable_list:
            sustainable_noun_phrases.extend(df['noun_phrases'].explode().tolist())
        elif address in RugPull_List:
            rugpull_noun_phrases.extend(df['noun_phrases'].explode().tolist())

    # 处理 result_dict_under_official
    for address, data in result_dict_under_official.items():
        df = pd.DataFrame(data).T.reset_index()
        valid_indices = pd.to_datetime(df['index'], errors='coerce').notna()
        df = df[valid_indices]
        
        df['index'] = pd.to_datetime(df['index'])
        df.set_index('index', inplace=True)

        df.index = df.index.astype('int64') // 10**9 // 3600
        df = df[~df.index.duplicated(keep='first')].sort_index()

        if address in Sustainable_list:
            sustainable_noun_phrases.extend(df['noun_phrases'].explode().tolist())
        elif address in RugPull_List:
            rugpull_noun_phrases.extend(df['noun_phrases'].explode().tolist())

    # 处理 result_dict
    for address, data in result_dict.items():
        df = pd.DataFrame(data).T.reset_index()
        valid_indices = pd.to_datetime(df['index'], errors='coerce').notna()
        df = df[valid_indices]
        
        df['index'] = pd.to_datetime(df['index'])
        df.set_index('index', inplace=True)

        df.index = df.index.astype('int64') // 10**9 // 3600
        df = df[~df.index.duplicated(keep='first')].sort_index()

        if address in Sustainable_list:
            sustainable_noun_phrases.extend(df['noun_phrases'].explode().tolist())
        elif address in RugPull_List:
            rugpull_noun_phrases.extend(df['noun_phrases'].explode().tolist())

    # 去掉 None 值和长度大于 10 的词
    sustainable_noun_phrases = [re.sub(r"[\[\]']", '', phrase) for phrase in sustainable_noun_phrases if phrase is not None and phrase != "" and len(phrase) <= 10]
    rugpull_noun_phrases = [re.sub(r"[\[\]']", '', phrase) for phrase in rugpull_noun_phrases if phrase is not None and phrase != "" and len(phrase) <= 10]
    # 生成词云
    sustainable_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(Counter(sustainable_noun_phrases))
    rugpull_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='plasma').generate_from_frequencies(Counter(rugpull_noun_phrases))

    # 显示词云
    plt.figure(figsize=(15, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(sustainable_wordcloud, interpolation='bilinear')
    plt.title('Sustainable Noun Phrases WordCloud')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(rugpull_wordcloud, interpolation='bilinear')
    plt.title('RugPull Noun Phrases WordCloud')
    plt.axis('off')

    plt.show()

# draw_word_cloud()

def get_img(time,chain):
    csv_file_folder = f"outputs/dex_scrape/chain_tweet_content_finish/{chain}_{time}"
    # D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/dex_scrape_moonshot_{time}_merge.csv
    img_save_dir =f"outputs/dex_scrape/chain_tweet_content_img/"
    # f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/images/{time}"
    if not os.path.exists(img_save_dir):
        os.makedirs(img_save_dir)

    result_dict = {}
    # 遍历官方文件夹下的所有子文件夹
    for dir_name in os.listdir(csv_file_folder):
        sub_dir_path = os.path.join(csv_file_folder, dir_name)
        if os.path.isdir(sub_dir_path):
            print(f"Processing Address: {sub_dir_path}")
            address = sub_dir_path.split('/')[-1]
            img_save_dir_folder= os.path.join(img_save_dir, address)
            if not os.path.exists(img_save_dir_folder):
                os.makedirs(img_save_dir_folder)
            
            for file_name in os.listdir(sub_dir_path):
                file_path = os.path.join(sub_dir_path, file_name)
                if file_name.endswith('.csv'):
                    print(f"Reading CSV file (Tweet Content): {file_path}")
                    df = pd.read_csv(file_path, sep=',', error_bad_lines=False)
                    for index, row in df.iterrows():
                        if row['Image']!="no found":
                            img_link = row['Image']
                            img_hash = row['Hash']
                            print(f"image_link: ========{img_link}===========")
                            file_name = os.path.splitext(img_link.split('/')[-1])[0]
                            cleaned_path=re.sub(r'[^a-zA-Z0-9]', '_', file_name)
                            img_path = os.path.join(img_save_dir_folder, img_hash)
                            try:
                                response = requests.get(img_link)
                                with open(img_path, 'wb') as file:
                                    file.write(response.content)
                                print(f"Image saved: {img_path}")
                                sleep(2)
                            except:
                                continue

# get_img("0828","solana")






def calculate_similarity(node1, node2):
    edges = []
    for date1 in node1['Postdate']:
        for date2 in node2['Postdate']:
            if abs(date1 - date2) <= timedelta(hours=1):
                sentiment1 = node1['text_sentiment'][date1]
                sentiment2 = node2['text_sentiment'][date2]
                if abs(sentiment1)>0 and abs(sentiment2)>0:
                    if abs(sentiment1 - sentiment2) <= 0.1:
                        edges.append((node1['account_name'], node2['account_name'], {'weight': 1}))
    return edges



def build_tweet_network(folder_path):
    G = nx.Graph()
    nodes = {}
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        address = os.path.basename(item_path)
        if os.path.isdir(item_path):
            for file in os.listdir(item_path):
                if file.endswith(".csv"):
                    file_path = os.path.join(item_path, file)
                    try:
                        df = pd.read_csv(file_path)
                        df['Postdate'] = pd.to_datetime(df['Postdate'], errors='coerce')
                        df = df.dropna(subset=['Postdate', 'AccountName'])
                        df = df[df['AccountName'] != 'no_scrape']
                        df = df[df['Postdate'] != 'no_scrape']
                        for index, row in df.iterrows():
                            account_name = row['AccountName']
                            postdate = row['Postdate']
                            text_sentiment = row['text_sentiment']
                            if account_name not in nodes:
                                nodes[account_name] = {
                                    'account_name': account_name,
                                    'addr': {address},
                                    'tweetid': {file_path},
                                    'Postdate': {postdate: text_sentiment},
                                    'text_sentiment': {postdate: text_sentiment}
                                }
                                G.add_node(account_name, addr=address)
                            else:
                                nodes[account_name]['addr'].add(address)
                                nodes[account_name]['tweetid'].add(file_path)
                                nodes[account_name]['Postdate'][postdate] = text_sentiment
                                nodes[account_name]['text_sentiment'][postdate] = text_sentiment
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
    for account_name, attributes in nodes.items():
        nx.set_node_attributes(G, {account_name: attributes})
    # 计算边
    node_keys = list(nodes.keys())
    total_pairs = len(node_keys) * (len(node_keys) - 1) // 2
    with tqdm(total=total_pairs, desc="Calculating edges") as pbar:
        for node1 in nodes.keys():
            for node2 in nodes.keys():
                if node1 != node2:
                    edges = calculate_similarity(nodes[node1], nodes[node2])
                    for edge in edges:
                        G.add_edge(edge[0], edge[1], weight=edge[2]['weight'])
                    pbar.update(1)
    
    return G

def save_graph_to_csv(G, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 保存节点属性
    nodes_data = {node: G.nodes[node] for node in G.nodes()}
    nodes_df = pd.DataFrame.from_dict(nodes_data, orient='index')
    nodes_df.index.name = 'node'
    nodes_df.to_csv(os.path.join(output_folder, 'nodes.csv'))
    
    # 保存边连接
    edges_data = [(u, v, d) for u, v, d in G.edges(data=True)]
    edges_df = pd.DataFrame(edges_data, columns=['source', 'target', 'attributes'])
    edges_df.to_csv(os.path.join(output_folder, 'edges.csv'), index=False)

# folder_path = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\dex_scrape\\chain_tweet_content_finish\\solana_0828"
# G = build_tweet_network(folder_path)

# output_folder = "D:\\Research_PostGraduate\\web3\\tweet\\outputs\\graph_csv_outputs"
# save_graph_to_csv(G, output_folder)

def form_gexf_file():
    # 读取 edge.csv 文件
    edge_df = pd.read_csv('outputs/graph_csv_outputs/edges.csv')

    # 读取 node.csv 文件
    node_df = pd.read_csv('outputs/graph_csv_outputs/node.csv')

    # 创建一个空的有向图
    G = nx.DiGraph()

    # 添加边到图中
    for index, row in edge_df.iterrows():
        source = row['source']
        target = row['target']
        attributes = eval(row['attributes'])  # 将字符串转换为字典
        G.add_edge(source, target, **attributes)

    # 添加节点到图中
    for index, row in node_df.iterrows():
        node = row['node']
        addr = eval(row['addr'])  # 将字符串转换为集合
        account_name = row['account_name']
        tweetid = eval(row['tweetid'])  # 将字符串转换为集合
        Postdate = eval(row['Postdate'])  # 将字符串转换为字典
        text_sentiment = eval(row['text_sentiment'])  # 将字符串转换为字典
        
        # 添加节点及其属性
        G.add_node(node, addr=addr, account_name=account_name, tweetid=tweetid, Postdate=Postdate, text_sentiment=text_sentiment)

    # 将图保存为 GEXF 文件
    nx.write_gexf(G, 'graph.gexf')

    print("GEXF 文件已成功生成！")
form_gexf_file()
# nx.write_gml(G, "tweet_network.gml")


import random
import matplotlib.colors as mcolors
def graph_analysis():

    # 读取 GML 文件
    # 读取 GML 文件
    G = nx.read_gml("tweet_network.gml")
    def print_base():
        print(f"Number of nodes: {G.number_of_nodes()}")

        # 打印边数量
        print(f"Number of edges: {G.number_of_edges()}")
        # 获取度数最高的10个节点
        top_nodes = [node for node, degree in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:10]]
        print(top_nodes)
        for node in top_nodes:
            print(f"Node {node} attributes: {G.nodes[node]}")
        # # 打印节点列表
        # print(f"Nodes: {list(G.nodes())}")

        # # 打印边列表
        # print(f"Edges: {list(G.edges())}")

        # 打印度分布
        # print(f"Degree distribution: {dict(G.degree())}")

        # # 打印平均度
        # print(f"Average degree: {nx.average_degree_connectivity(G)}")

        # # 打印图的密度
        # print(f"Graph density: {nx.density(G)}")
    print_base()
    def frequency_draw():
        degrees = [degree for node, degree in G.degree()]

        # 设置直方图的 bin 数量
        num_bins = 100

        # 绘制频率分布图
        plt.figure(figsize=(10, 6))
        n, bins, patches = plt.hist(degrees, num_bins, density=True, facecolor='turquoise', alpha=0.75)

        # 添加标题和标签
        plt.title('Degree Frequency Distribution')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')

        # 显示图形
        plt.show()
    # frequency_draw()
    def networkdx_draw():
    # 读取 GML 文件

        # 获取度数最高的10个节点
        top_nodes = [node for node, degree in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:10]]
        print(top_nodes)
        for node in top_nodes:
            print(f"Node {node} attributes: {G.nodes[node]}")
        # 扩展选择：包含这些高度的节点及其直接邻居节点
        community_nodes = set(top_nodes)
        for node in tqdm(top_nodes, desc="Processing nodes"):
            community_nodes.update(G.neighbors(node))

        # 过滤掉度数为零的节点
        community_nodes = {node for node in community_nodes if G.degree(node) > 0}

        # 创建子图
        subgraph = G.subgraph(community_nodes)

        # 假设 text_sentiment 是一个字典，键是节点，值是该节点的 text_sentiment 均值
        text_sentiment = {node: G.nodes[node].get('text_sentiment', 0) for node in subgraph.nodes}

        # 获取 text_sentiment 均值的范围
        sentiment_values = list(text_sentiment.values())
        vmin = min(sentiment_values)
        vmax = max(sentiment_values)
        print(vmin)
        print(vmax)
        if vmax == vmin:
            vmax += 1e-6

        cmap = plt.cm.get_cmap('coolwarm')

        plt.figure(figsize=(16, 16))
        pos = nx.spring_layout(subgraph, k=0.3, iterations=500)  # 使用 spring_layout 布局
        ax = plt.gca()

        node_colors = [cmap((text_sentiment[node] - vmin) / (vmax - vmin)) for node in subgraph.nodes]
        nx.draw_networkx_nodes(subgraph, pos, node_size=1000, node_color=node_colors, edgecolors='none', linewidths=0, ax=ax)  # 去掉边框

        nx.draw_networkx_edges(subgraph, pos, edge_color='gray', style='dashed', alpha=0.6, ax=ax)  # 调整边样式

        nx.draw_networkx_labels(subgraph, pos, font_size=10, font_color='black', font_weight='bold', ax=ax)

        plt.title("Community of High Degree Nodes and Their Neighbors", fontsize=20, fontweight='bold')
        plt.axis('off')  # 去掉坐标轴
        plt.show()
    # networkdx_draw()
    def cen():
        degree_centrality = nx.degree_centrality(G)
        closeness_centrality = nx.closeness_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        eigenvector_centrality = nx.eigenvector_centrality(G)
    

# graph_analysis()