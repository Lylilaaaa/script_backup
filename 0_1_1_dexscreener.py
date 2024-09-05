from bs4 import BeautifulSoup  # 从bs4模块中导入BeautifulSoup类，用于解析HTML
import csv  # 导入csv模块，用于读写CSV文件
from selenium import webdriver
import undetected_chromedriver as uc
import requests
from datetime import datetime, timedelta
from selenium import __version__
from DrissionPage import ChromiumPage
from time import sleep
import pandas as pd
import os
from tqdm import tqdm
from Scweet.scweet import scrape
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import random
import shutil
import hashlib
import re
import math
print(f"Selenium version: {__version__}")
# options= Options() 

# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.get('https://coinmarketcap.com/view/memes/?page=1')
user_agent_list = [
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16"
]
def init_driver(headless=False, proxy="http://127.0.0.1:7890"):
    """ initiate a chromedriver or firefoxdriver instance
        --option : other option to add (str)
    """

    chroptions = webdriver.ChromeOptions()
    # driver_path = ChromeDriverManager().install()

    if headless is True:
        print("Scraping on headless mode.")
        chroptions.add_argument('--disable-gpu')
        chroptions.headless = True
    else:
        chroptions.headless = False
    # chroptions.add_argument("start-maximized")
    chroptions.add_argument('log-level=3')

    if proxy is not None:
        chroptions.add_argument('--proxy-server=%s' % proxy)
        print("using proxy : ", proxy)

    
    chroptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    print("add option : excludeSwitches")
    chroptions.add_experimental_option('useAutomationExtension', False)
    print("add option : useAutomationExtension")


    # user_agent = random.choice(user_agent_list)
    # options.add_argument(f'user-agent={user_agent}')

    #driver = webdriver.Chrome(service=Service(driver_path), options=options)  # 修改此行以添加代理
    driver = uc.Chrome(options=chroptions)
    print("driver : uc.Chrome(options=chroptions)")

    return driver

def read_whole_page_moonshot(time):
    p = ChromiumPage()
    p.get('https://dexscreener.com/moonshot')
    sleep(20)

    soup = BeautifulSoup(p.html, 'html.parser')

    a_herfs = soup.find_all('a',{'class':'custom-1l5wjfu'})
    # for atag in a_herfs:
    #     print(atag)
    num_rows = len(a_herfs)
    print("Number of rows:", num_rows)
    data = []  # 创建一个空列表，用于存储解析后的数据
    for row in a_herfs:  # 遍历每一行
        # find link of solana
        try:
            link_elem = row['href']
            link = link_elem
            # link_elem = row.find('a',  attrs={'class': "custom-1l5wjfu"},href = True).attrs['href']  # 获取货币link
            # link = link_elem
        except AttributeError:
            print("connot find the link!")
            link = ''
        # find http img link
        try:
            img_elem = row.find('img', attrs={'class': "chakra-image custom-v0rs9q"}, src = True)  # 获取货币大写缩写
            img = img_elem
        except AttributeError:
            img = ''
        # find coin simple name
        try:
            name_simple_elem = row.find('span', {'class': 'chakra-text custom-1h1xtdz'}).text.strip() 
            name_simple = name_simple_elem
        except AttributeError:
            name_simple = ''
        # find coin long name
        try:
            name_elem = row.find('span', {'class': 'chakra-text custom-1c2lit1'}).text.strip() 
            name = name_elem
        except AttributeError:
            name = ''
        # find para
        try:
            par_elem = row.find('p', {'class': 'chakra-text custom-h4zz0d'}).text.strip() 
            par = par_elem
        except AttributeError:
            par = '' 
        data.append({'Name_simple':name_simple ,'Name_long':name,'Img_link': img,'Link': link,'Describe': par})  # 将获取的数据添加到列表中

    with open(f'outputs/dex_scrape/dex_scrape_moonshot_{time}.csv', 'w', newline='',encoding='utf-8') as csvfile:  # 打开CSV文件进行写操作
        fieldnames = ['Name_simple', 'Name_long','Img_link','Link','Describe']  # 设置CSV文件的列名列表
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # 创建CSV写入对象

        writer.writeheader()  # 写入CSV文件的头部（列名）
        for d in data:  # 遍历每一条数据
            writer.writerow(d)  # 写入数据到CSV文件
    p.quit()
    # data = driver.page_source
    # driver.quit()
def read_whole_page_diff_chain(time,chain):
    p = ChromiumPage()
    p.get(f'https://dexscreener.com/{chain}')
    sleep(20)

    soup = BeautifulSoup(p.html, 'html.parser')

    a_herfs = soup.find_all('a',{'class':'ds-dex-table-row ds-dex-table-row-top'})
    # for atag in a_herfs:
    #     print(atag)
    num_rows = len(a_herfs)
    print("Number of rows:", num_rows)
    data = []  # 创建一个空列表，用于存储解析后的数据
    for row in a_herfs:  # 遍历每一行
        # find link of solana
        try:
            link_elem = row['href']
            link = link_elem
        except AttributeError:
            print("connot find the link!")
            link = ''
        # find http img link
        try:
            img_elem = row.find('img', attrs={'class': "ds-dex-table-row-token-icon"}, src = True)  
            img = img_elem
        except AttributeError:
            img = ''
        # find coin simple name
        try:
            name_simple_elem = row.find('span', {'class': 'ds-dex-table-row-base-token-symbol'}).text.strip() 
            name_simple = name_simple_elem
        except AttributeError:
            name_simple = ''
        # find coin long name
        try:
            name_elem = row.find('span', {'class': 'ds-dex-table-row-base-token-name'}).text.strip() 
            name = name_elem
        except AttributeError:
            name = ''
        
        data.append({'Name_simple':name_simple ,'Name_long':name,'Img_link': img,'Link': link})  # 将获取的数据添加到列表中

    with open(f'outputs/dex_scrape/chain/dex_scrape_{chain}_{time}.csv', 'w', newline='',encoding='utf-8') as csvfile:  # 打开CSV文件进行写操作
        fieldnames = ['Name_simple', 'Name_long','Img_link','Link','Describe']  # 设置CSV文件的列名列表
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # 创建CSV写入对象

        writer.writeheader()  # 写入CSV文件的头部（列名）
        for d in data:  # 遍历每一条数据
            writer.writerow(d)  # 写入数据到CSV文件
    p.quit()
    # data = driver.page_source
    # driver.quit()

def read_detailed_page(time,chain):
    # read data file
    date_list_path = f"outputs/dex_scrape/chain/dex_scrape_{chain}_{time}.csv"
    date_df = pd.read_csv(date_list_path)
    data = []
    link_list = date_df['Link'].tolist()
    for _link in link_list:
        p = ChromiumPage()
        p.get(f'https://dexscreener.com{_link}')
        sleep(3)
        soup = BeautifulSoup(p.html, 'html.parser')

        # find twitter link
        try:
            social_links = soup.find_all('a', {'class': 'chakra-link chakra-button custom-1xt6654'})
            social_link_array = []
            if social_links:
                for link in social_links:
                    href = link.get('href')
                    if href:
                        social_link_array.append(href)
                    else:
                        print("No Href in social media link.")
            else:
                print("No social links found.")
        except AttributeError:
            social_link_array = []

        # find price
        try:
            price_elem = soup.find('div', {'class': "custom-1baulvz"}).text.strip()
            price = price_elem
        except AttributeError:
            price = ''

        # find price percentage
        try:
            price_dyn_array = []
            price_dyn_elems = soup.find_all('span', {'class': "chakra-text custom-160j8xt"})
            for price_syn in price_dyn_elems:
                text_elem = price_syn.get_text()
                price_dyn_array.append(text_elem)
        except AttributeError:
            price_dyn_array = []

        # find VOLUME
        try:
            volume_array = []
            volume_elems = soup.find_all('div', {'class': 'chakra-stack custom-16409fq'})
            for volume_elem in volume_elems:
                text_elem = volume_elem.get_text()
                volume_array.append(text_elem)
        except AttributeError:
            volume_array = []

        # find other attitude:
        try:
            attitude_array = []
            attitude_elem = soup.find("div", {"class": "chakra-button__group custom-ndy15h"})
            att_ele=  attitude_elem.find_all("div",{"class":"chakra-stack custom-18e1wj0"})
            for ele in att_ele:
                attitude_array.append(ele.get_text())
        except AttributeError:
            attitude_array = []

        # find detailed describe:
        try:
            describe_elem = soup.find("p", {"class": "chakra-text custom-nn0azp"})
            describe = describe_elem.get_text()
        except AttributeError:
            describe = ""

        # 将获取的数据添加到字典中
        page_data = {
            'Link':_link,
            'Total_Describe': describe,
            'Price': price,
            'Price_Percentage': price_dyn_array,
            'Volume': volume_array,
            'Attitude': attitude_array,
            'Social_Links': social_link_array
        }
        data.append(page_data)

    # 将数据写入CSV文件
    with open(f'outputs/dex_scrape/chain/dex_scrape_{chain}_{time}_detailed.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Link', 'Total_Describe', 'Price', 'Price_Percentage', 'Volume', 'Attitude', 'Social_Links']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in data:
            writer.writerow(d)

        p.quit()



def merge_file(time,chain):
    csv_file1 = f"outputs/dex_scrape/chain/dex_scrape_{chain}_{time}_detailed.csv"
    csv_file2 = f"outputs/dex_scrape/chain/dex_scrape_{chain}_{time}.csv"

    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    merged_df = pd.merge(df1, df2, on='Link', how='outer')

    output_file = f"outputs/dex_scrape/chain/dex_scrape_{chain}_{time}_merge.csv"
    merged_df.to_csv(output_file, index=False)


def save_img(time,chain):
    csv_file = f"outputs/dex_scrape/chain/dex_scrape_{chain}_{time}_merge.csv"
    # D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/dex_scrape_moonshot_{time}_merge.csv
    df = pd.read_csv(csv_file)
    img_save_dir = f"outputs/dex_scrape/chain_img/{chain}_{time}"
    # f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/images/{time}"
    if not os.path.exists(img_save_dir):
        os.makedirs(img_save_dir)
    total_images = len(df)
    start_index = 93
    for index, row in tqdm(df.iterrows(), total=total_images, unit="image", desc="Downloading images"):
        if index < start_index:
            continue
        img_link = row['Img_link']
        link = row['Link']
        if not isinstance(img_link, str):
            continue
        soup = BeautifulSoup(img_link, 'html.parser')
        img_tag = soup.find('img')
        img_link = img_tag['src'] if img_tag else None

        print(img_link)
        file_name = os.path.splitext(link.split('/')[-1])[0]
        img_path = os.path.join(img_save_dir, file_name)
        response = requests.get(img_link)
        with open(img_path, 'wb') as file:
            file.write(response.content)

        print(f"Image saved: {img_path}")
        sleep(2)
# read_whole_page_diff_chain("0828","solana")
# read_detailed_page("0828","solana")
# merge_file("0828","solana")
# save_img("0828","solana")


def merge_data_csv():
    csv_folder_path = "D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/detailed"
    csv_names = os.listdir(csv_folder_path)
    merged_df = pd.DataFrame()
    for csv_name in csv_names:
        csv_path = os.path.join(csv_folder_path, csv_name)
        detailed_df = pd.read_csv(csv_path)
        merged_df = pd.concat([merged_df, detailed_df], ignore_index=True)
    merged_df = merged_df.drop_duplicates(subset=['Link'], keep='last')
    merged_df["Address"] = merged_df["Link"].str.split('/').str[-1]
    merged_df.to_csv("D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/merge/dex_scrape_merge.csv", index=False)  

# merge_data_csv()

def merge_data_image():
    # 读取两个 DataFrame
    image_index_df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/merge/image_index.csv")
    dex_scrape_df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/merge/dex_scrape_merge.csv")

    merged_df = pd.merge(image_index_df, dex_scrape_df, left_on="filename", right_on="Address", how="inner")

    # 输出合并后的 DataFrame
    merged_df.to_csv("D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/merge/info_image_merge.csv", index=False)

# merge_data_image()
def get_twitter_list(time,chain):
    meme_list_df = pd.read_csv(f"outputs/dex_scrape/chain/dex_scrape_{chain}_{time}_merge.csv")
    meme_list_df['Social_Links'] = meme_list_df['Social_Links'].str.replace("[", "").str.replace("]", "")
    meme_list_df['Social_Links'] = meme_list_df['Social_Links'].str.replace("'", "")
    meme_list_df['Twitter_link'] = ''
    for i, ele in enumerate(meme_list_df['Social_Links']):
        social_list = ele.split(',')
        for link in social_list:
            if 'x.com' in link or 'twitter.com' in link:
                meme_list_df.at[i, 'Twitter_link'] = link.strip()
                break
    print(meme_list_df['Twitter_link'])
    meme_list_df['Twitter_id'] = meme_list_df['Twitter_link'].apply(lambda x: x.split('/')[-1] if isinstance(x, str) else x)
    for i, ele in enumerate(meme_list_df['Twitter_id']):
        if ele == "" or ele == "'":
            try:
                meme_list_df.at[i, 'Twitter_link'] = ele.split('/')[-2]
            except:
                continue
    meme_list_df.to_csv(f"outputs/dex_scrape/chain/dex_scrape_{chain}_{time}_merge.csv", index=False)


def scape_tweet(address,tweet_id,link,time,chain):
    p = ChromiumPage()
    p.get(link)
    sleep(4)
    soup = BeautifulSoup(p.html, 'html.parser')
    if "This account doesn’t exist" in soup.get_text() or "This account doesn't exist" in soup.get_text():
        return "NOT EXIST ACCOUNT","0","0"
    p.get(f"{link}/media")
    sleep(6)
    for i in range(1, 10):
        p.scroll.to_bottom()
        sleep(1)
    soup = BeautifulSoup(p.html, 'html.parser')
    media_list = soup.find_all('li',{'role':'listitem'})

    data = []  
    index = 0
    for row in media_list:  # 遍历每一行
        
        # find image link
        try:
            img_link_ele = row.find('a', href = True).attrs['href']  
            img_link = img_link_ele
        except AttributeError:
            img_link = ''
        # find image
        try:
            image_ele = row.find('img',src = True).attrs['src'] 
            image = image_ele
        except AttributeError:
            image = ''

        data.append({'Address':address ,'Tweet':tweet_id,"Img_index":index,'Img_link': img_link,'Img': image})  # 将获取的数据添加到列表中
        index += 1

    with open(f'outputs/dex_scrape/chain_tweet_img/{chain}_{time}/dex_scrape_tweet_{address}.csv', 'w', newline='',encoding='utf-8') as csvfile:  # 打开CSV文件进行写操作
        fieldnames = ['Address', 'Tweet','Img_index','Img_link','Img']  # 设置CSV文件的列名列表
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # 创建CSV写入对象

        writer.writeheader() 
        for d in data: 
            writer.writerow(d) 

    return

def scape_tweet_just_followers(link):
    p = ChromiumPage()
    p.get(link)
    sleep(4)
    soup = BeautifulSoup(p.html, 'html.parser')
    if "This account doesn’t exist" in soup.get_text() or "This account doesn't exist" in soup.get_text():
        return "NOT EXIST ACCOUNT","0","0"
    sleep(6)
    for i in range(1, 10):
        p.scroll.to_bottom()
        sleep(1)
    soup = BeautifulSoup(p.html, 'html.parser')

    # find twitter describe
    try:
        des_ele = soup.find_all('div',{'class': "css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41"})
        if len(des_ele) == 0:
            return "NO DESCRIBE","0","0"
        des_text = des_ele[1].get_text()
    except AttributeError:
        des_text = ''

    try: 
        following_ele = soup.find_all('span',{'class':"css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-1b43r93 r-1cwl3u0 r-b88u0q"})
        if len(following_ele) == 0:
            return "NO FOLLOWER","0","0"
        # print(f"following_ele:{following_ele}")
        if len(following_ele) > 0:
            following_text = following_ele[0].get_text()
        else:
            following_text = ''
        if len(following_ele) > 1:
            follower_text = following_ele[1].get_text()
        else:
            follower_text = ''
    except  AttributeError:
        following_text = ''
        follower_text = ''
    return  des_text,following_text,follower_text


def start_scrape(time,chain):
    get_twitter_list(time,chain)
    meme_list_df = pd.read_csv(f"outputs/dex_scrape/chain/dex_scrape_{chain}_{time}_merge.csv", encoding='latin-1')
    link_list = meme_list_df['Twitter_link'] 
    id_list = meme_list_df['Twitter_id'] 
    meme_list_df["Address"] = meme_list_df["Link"].str.split('/').str[-1]
    address_list = meme_list_df['Address'] 
    index = 0
    # login my tweet
    # p = ChromiumPage()
    # sleep(60)
    # p.quit()
    for i in tqdm(range(index, len(link_list)), total=len(link_list) - index, desc="Scraping tweets"):
        ele = link_list[i]
        # scape_tweet(address_list[i],id_list[i],ele,time,chain)
        des_text_,following_text_,follower_text_ = scape_tweet_just_followers(ele)
        meme_list_df.at[i, 'Des_text'] = des_text_
        meme_list_df.at[i, 'Following_text'] = following_text_
        meme_list_df.at[i, 'Follower_text'] = follower_text_
        meme_list_df.to_csv(f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/chain_tweet_account/{chain}_{time}/info_tweet_updated7.csv", index=False)
# start_scrape("0828","solana")

# merge the account we got
def merge_tweet_account(time,chain):
    csv_folder_path = f"outputs/dex_scrape/chain_tweet_account/{chain}_{time}"
    csv_names = os.listdir(csv_folder_path)
    merged_df = pd.DataFrame()
    for csv_name in csv_names:
        csv_path = os.path.join(csv_folder_path, csv_name)
        detailed_df = pd.read_csv(csv_path)
        detailed_df = detailed_df[(detailed_df['Follower_text'].notna()) & (detailed_df['Following_text'].notna())]
        merged_df = pd.concat([merged_df, detailed_df], ignore_index=True)
    merged_df = merged_df.drop_duplicates(subset=['Link'], keep='last')
    merged_df.to_csv(f"outputs/dex_scrape/chain_tweet_account/{chain}_{time}/info_tweet_updated.csv", index=False)  
# merge_tweet_account("0828","solana")

def temp_delete():
    df1 = pd.read_csv(f"outputs/dex_scrape/chain_tweet_account/solana_0828/info_tweet_updated.csv")
    df2 = pd.read_csv(f"outputs/dex_scrape/chain_tweet_account/info_tweet_updated.csv",encoding='ISO-8859-1')
    if 'Link' not in df1.columns or 'Link' not in df2.columns:
        raise ValueError("'key_column' not found in one or both of the DataFrames")
    df1_filtered = df1[df1['Link'].isin(df2['Link'])]
    df1_filtered.to_csv(f"outputs/dex_scrape/chain_tweet_account/solana_0828/info_tweet_updated.csv", index=False)
# temp_delete()


# filter the useless account after detete them by hands
# chain_tweet_account=>chain_tweet_img_filter=>
def filter_img_folder(time,chain):
    csv_path = f'outputs/dex_scrape/chain_tweet_account/{chain}_{time}/info_tweet_updated.csv'
    df = pd.read_csv(csv_path)
    addresses = df['Address']

    source_folder = f'outputs/dex_scrape/chain_tweet_img/{chain}_{time}'
    target_folder = f'outputs/dex_scrape/chain_tweet_img_filter/{chain}_{time}'
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for address in addresses:
        source_file = os.path.join(source_folder, f'dex_scrape_tweet_{address}.csv')
        if os.path.exists(source_file):
            target_file = os.path.join(target_folder, f'dex_scrape_tweet_{address}.csv')
            shutil.move(source_file, target_file)
            print(f'Moved {source_file} to {target_file}')
        else:
            print(f'File not found: {source_file}')
# filter_img_folder("0828","solana")


def delete_all_file_under(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path) 
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path) 
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        print(f'The directory {folder_path} does not exist.') 


# chain_tweet_account=>chain_tweet_img_filter=>chain_tweet_content
def get_tweet_cointent_tweet(time,chain):
    content_saving_folder = f'outputs/dex_scrape/chain_tweet_content/{chain}_{time}'
    if not os.path.exists(content_saving_folder):
        os.makedirs(content_saving_folder)
    content_reading_folder = f'outputs/dex_scrape/chain_tweet_img_filter/{chain}_{time}'
    all_files = os.listdir(content_reading_folder)
    meme_file_list = [file for file in all_files if file.endswith('.csv')]

    for filename in meme_file_list:
        meme_addr = filename.replace('.csv', '').split('_')[-1]
        add_X_saving_folder = f'outputs/dex_scrape/chain_tweet_content/{chain}_{time}/{meme_addr}'
        if not os.path.exists(add_X_saving_folder):
            os.makedirs(add_X_saving_folder)
        delete_all_file_under(add_X_saving_folder)
        file_path = os.path.join(content_reading_folder, filename)
        tweet_list_df = pd.read_csv(file_path)
        link_list = tweet_list_df["Img_link"] # /UnrevealedXYZ/status/1788177487320567961/photo/1
        # https://x.com/UnrevealedXYZ/status/1787897217145049180 => real link
        for link in link_list:
            start_time =  datetime.now()
            file_name = link.replace("/", "_")
            data = []
            hash_array = []
            x_link = f"https://x.com{link}"
            print(f"====================get link: ================={x_link}")
            max_retries = 10  # 设置最大重试次数
            retries = 0
            p = ChromiumPage()
            p.get(x_link)
            while retries < max_retries:
                p = ChromiumPage()
                p.get(x_link)
                
                sleep(1)
                # should get the num of comments of this tweet first

                soup = BeautifulSoup(p.html, 'html.parser')
                post_ele = soup.find_all('article')
                
                if len(post_ele) > 0:
                    card = post_ele[0]
                    # 继续处理 card
                    print("Found the article element.")
                    break
                else:
                    retries += 1
                    sleep(2)  # 等待一段时间后重试
                    print(f"Retrying... ({retries}/{max_retries})")
            
            if retries == max_retries:
                print("Failed to find the article element after maximum retries.")
            soup = BeautifulSoup(p.html, 'html.parser')
            post_ele = soup.find_all('article')
            print(len(post_ele))
            card = post_ele[0]

            # username
            username = "no_scrape"
            try:
                span_element = card.find('span', text=lambda x: x and '@' in x)
                if span_element:
                    username = span_element.text
            except:
                username = "error"
            print(f"Username: {username}")
            # postdate
            postdate = "no_scrape"
            try:
                time_element = card.find('time')
                if time_element and time_element.has_attr('datetime'):
                    postdate = time_element['datetime']
            except:
                postdate = "error"
            print(f"Postdate: {postdate}")
            # text
            text = "no_scrape"
            try:
                div_element = card.find("div", {"data-testid": "tweetText"})
                if div_element:
                    text = div_element.get_text()
            except:
                text = "error"
            print(f"Text: {text}")

            # unique hash
            combined_string = f"{username}_{postdate}_{text}"
            print(f"=========origin tweet======={combined_string}")
            hash_object = hashlib.sha256(combined_string.encode())
            unique_hash = hash_object.hexdigest()
            hash_array.append(unique_hash)

            # article type
            article_type = "none"
            article_type = "origin"

            # img
            img = "none"
            try:
                img_element = card.find("img", {"alt": "Image"}).attrs['src'] 
                if img_element:
                    img = img_element
            except:
                img = "no found"
            print(f"img: {img}")  

            # video
            video = "none"
            try:
                video_element = card.find("video").attrs['poster'] 
                if video_element:
                    video = video_element
            except:
                video = "no found"
            print(f"video: {video}")  


            # comments, retweets, likes, marks
            comment_array = "none"
            try:
                comment_element = card.find("div", {"role": "group"}).attrs['aria-label'] 
                if comment_element:
                    comment_array = comment_element
            except:
                comment_array = "no found"
            print(f"comment group: {comment_array}")  

            # data.append({'AccountName':username ,'Postdate':postdate,"Text":text,"Hash":unique_hash,"Type":article_type,'Image': img,'Video': video,'CommentGroup': comment_array})  # 将获取的数据添加到列表中
            origin_ow = {'AccountName':username ,'Postdate':postdate,"Text":text,"Hash":unique_hash,"Type":article_type,'Image': img,'Video': video,'CommentGroup': comment_array}
            with open(f'{add_X_saving_folder}/{file_name}.csv', 'w', newline='',encoding='utf-8') as csvfile:
                fieldnames = ['AccountName', 'Postdate','Text','Hash','Type','Image','Video','CommentGroup'] 
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
                writer.writeheader() 
                writer.writerow(origin_ow) 
                print("+++++++++++++ORIGIN TWEET WRITED!!+++++++++++++")

            # reweet:/retweets
            replies_count = 0
            if comment_array:
                replies_match = re.search(r"(\d+)\s+replies", comment_array)
                replies_count = int(replies_match.group(1)) if replies_match else 0
            scroll_num = math.ceil(replies_count/15) 
            print(f"=== replies cointing ==={replies_count}")
            # # then scrape all comments
            hash_frequency = {}
            scrolling_index = 0
            for i in range(1, replies_count):
                print(f"===============scrolling================={scrolling_index}")
                scrolling_index+=1
                
                #p.scroll.to_bottom()
                should_break = False
                soup = BeautifulSoup(p.html, 'html.parser')

                try:
                    ele = p.ele('Show probable spam')
                    ele.click(by_js=None)
                except:
                    pass

                try:
                    eles_ = p.eles('tag:button')
                    for e in eles_:
                        size = e.rect.size
                        width, height = size
                        if 62 <= width <= 63 and 31 <= height <= 33: 
                            e.click(by_js=None)
                except:
                    pass



                # post_ele = soup.find_all('article',{'data-testid':'tweet'})
                post_ele = soup.find_all('article')
                print(f"============================POST ELE COUNT: {len(post_ele)}")
                for key_hash in hash_frequency:
                    if hash_frequency[key_hash] >= 5:
                        # print(f"Hash {key_hash} has appeared 5 times. Breaking loop.")
                        should_break = True
                        break
                if should_break:
                    print("should break here")
                    break
                for card in post_ele:
                    # username
                    username = "no_scrape"
                    try:
                        span_element = card.find('span', text=lambda x: x and '@' in x)
                        if span_element:
                            username = span_element.text
                    except:
                        username = "error"
                    print(f"Username: {username}")
                    # postdate
                    postdate = "no_scrape"
                    try:
                        time_element = card.find('time')
                        if time_element and time_element.has_attr('datetime'):
                            postdate = time_element['datetime']
                    except:
                        postdate = "error"
                    print(f"Postdate: {postdate}")
                    # text
                    text = "no_scrape"
                    try:
                        div_element = card.find("div", {"data-testid": "tweetText"})
                        if div_element:
                            text = div_element.get_text()
                    except:
                        text = "error"
                    print(f"Text: {text}")

                    # unique hash
                    combined_string = f"{username}_{postdate}_{text}"
                    hash_object = hashlib.sha256(combined_string.encode())
                    unique_hash = hash_object.hexdigest()

                    if unique_hash not in hash_frequency:
                        hash_frequency[unique_hash] = 1

                    if unique_hash in hash_array:
                        hash_frequency[unique_hash] += 1
                        continue
                    else:
                        hash_array.append(unique_hash)

                    # article type
                    article_type = "none"
                    article_type = "reply"

                    # img
                    img = "none"
                    try:
                        img_element = card.find("img", {"alt": "Image"}).attrs['src'] 
                        if img_element:
                            img = img_element
                    except:
                        img = "no found"
                    print(f"img: {img}")  

                    # video
                    video = "none"
                    try:
                        video_element = card.find("video", {"playsinline aria-label": "Embedded video"}).attrs['poster'] 
                        if video_element:
                            video = video_element
                    except:
                        video = "no found"
                    print(f"video: {video}")  


                    # comments, retweets, likes, marks
                    comment_array = "none"
                    try:
                        comment_element = card.find("div", {"role": "group"}).attrs['aria-label'] 
                        if comment_element:
                            comment_array = comment_element
                    except:
                        comment_array = "no found"
                    print(f"comment group: {comment_array}")  
                            
                    data.append({'AccountName':username ,'Postdate':postdate,"Text":text,"Hash":unique_hash,"Type":article_type,'Image': img,'Video': video,'CommentGroup': comment_array})  # 将获取的数据添加到列表中
                p.scroll.down(2000)

                sleep(0.5)
            # origin_ow = {'AccountName':username ,'Postdate':postdate,"Text":text,"Hash":unique_hash,"Type":article_type,'Image': img,'Video': video,'CommentGroup': comment_array}
            with open(f'{add_X_saving_folder}/{file_name}.csv', 'a', newline='',encoding='utf-8') as csvfile:
                fieldnames = ['AccountName', 'Postdate','Text','Hash','Type','Image','Video','CommentGroup'] 
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
                for d in data:
                    writer.writerow(d) 
            end_time =  datetime.now()
            elapsed_time = end_time - start_time  # 计算耗时
            print(f"Total time elapsed: {elapsed_time.total_seconds():.2f} seconds")
# get_tweet_cointent_tweet("0828","solana")

def find_social_time_simple(time, chain):
    content_saving_folder = f'outputs/dex_scrape/chain_tweet_content_finish/{chain}_{time}'
    content_meme_folder = f'outputs/dex_scrape/chain_tweet_img_filter_finish/{chain}_{time}'
    all_folder = os.listdir(content_saving_folder)
    meme_folder_list = [meme_addr_folder for meme_addr_folder in all_folder if os.path.isdir(os.path.join(content_saving_folder, meme_addr_folder))]
    
    meme_addr_time_range = {}

    for meme_folder  in meme_folder_list:
        meme_folder_path = os.path.join(content_saving_folder, meme_folder)
        meme_tweet_content_list = [meme_file for meme_file in os.listdir(meme_folder_path) if meme_file.endswith(".csv")]
        all_postdates = []
        for meme_tweet_content in meme_tweet_content_list:
            content_path = os.path.join(meme_folder_path, meme_tweet_content)
            tweet_content_df = pd.read_csv(content_path)
            for postdate in tweet_content_df['Postdate'].tolist():
                try:
                    date = pd.to_datetime(postdate)
                    all_postdates.append(date)
                except (ValueError, TypeError):
                    continue

                
        if all_postdates:
            min_postdate = min(all_postdates)
            max_postdate = max(all_postdates)
            meme_addr_time_range[meme_folder] = (min_postdate, max_postdate)
    return meme_addr_time_range
def update_info_tweet_csv(time, chain, meme_addr_time_range):
    info_tweet_path = f'outputs/dex_scrape/chain_tweet_account/{chain}_{time}/info_tweet_updated.csv'
    info_tweet_df = pd.read_csv(info_tweet_path)
    
    info_tweet_df['start_time'] = info_tweet_df['Address'].map(lambda x: meme_addr_time_range.get(x, ('', ''))[0])
    info_tweet_df['end_time'] = info_tweet_df['Address'].map(lambda x: meme_addr_time_range.get(x, ('', ''))[1])
    
    info_tweet_df.to_csv(info_tweet_path, index=False)

time = '0828'
chain = 'solana'
# meme_addr_time_range = find_social_time_simple(time, chain) 
# find_social_time_simple("0828","solana")
# update_info_tweet_csv(time, chain, meme_addr_time_range)

# chain_tweet_account=>chain_tweet_img_filter=>chain_tweet_content
def find_tweet_community(time,chain):
    directory = os.path.dirname(f"outputs/dex_scrape/chain_tweet_community/{chain}_{time}/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    info_tweet_path = f'outputs/dex_scrape/chain_tweet_account/{chain}_{time}/info_tweet_updated_filter.csv'
    info_tweet_df = pd.read_csv(info_tweet_path, encoding='latin1')
    for index, row in info_tweet_df.iterrows():
        start_time = row['start_time']
        end_time = row['end_time']
        name_simple = row['Name_simple']
        if pd.to_datetime(start_time, errors='coerce') and pd.to_datetime(end_time, errors='coerce') and pd.notna(name_simple):
            start_time_dt = pd.to_datetime(start_time, errors='coerce')
            end_time_dt = pd.to_datetime(end_time, errors='coerce')
            if pd.isna(start_time_dt) or pd.isna(end_time_dt) or pd.isna(name_simple):
                continue

            current_start = start_time_dt
            while current_start < end_time_dt:
                current_end = current_start + timedelta(days=30)
                if current_end > end_time_dt:
                    current_end = end_time_dt

                # 生成Twitter搜索链接
                start_date = current_start.strftime('%Y-%m-%d')
                end_date = current_end.strftime('%Y-%m-%d')
                search_link = f"https://x.com/search?f=top&q=${name_simple}%20until%3A{end_date}%20since%3A{start_date}&src=typed_query"
                print(search_link)

                name_simple_clean = name_simple.replace('/', '_')
                add_X_saving_path = f'outputs/dex_scrape/chain_tweet_community/{chain}_{time}/{name_simple_clean}_{row["Address"]}.csv'
                start_time_ =  datetime.now()
                data = []
                hash_array = []
                print(f"====================get link: ================={search_link}")
                max_retries = 10 
                retries = 0
                p = ChromiumPage()
                p.get(search_link)
                while retries < max_retries:
                    p = ChromiumPage()
                    p.get(search_link)
                    
                    sleep(5)
                    # should get the num of comments of this tweet first

                    soup = BeautifulSoup(p.html, 'html.parser')
                    post_ele = soup.find_all('article')
                    print(f"length of the aticle: {len(post_ele)}")
                    if len(post_ele) > 0:
                        card = post_ele[0]
                        # 继续处理 card
                        print("Found the article element.")
                        break
                    else:
                        retries += 1
                        sleep(2)  # 等待一段时间后重试
                        print(f"Retrying... ({retries}/{max_retries})")
                if retries>=max_retries:
                    sleep(5*120)
                    retries = 0
                    while retries < max_retries:
                        p = ChromiumPage()
                        p.get(search_link)
                        
                        sleep(5)
                        # should get the num of comments of this tweet first

                        soup = BeautifulSoup(p.html, 'html.parser')
                        post_ele = soup.find_all('article')
                        print(f"length of the aticle: {len(post_ele)}")
                        if len(post_ele) > 0:
                            card = post_ele[0]
                            # 继续处理 card
                            print("Found the article element.")
                            break
                        else:
                            retries += 1
                            sleep(2)  # 等待一段时间后重试
                            print(f"Retrying... ({retries}/{max_retries})")
                if retries == max_retries:
                    print("Failed to find the article element after maximum retries.")
                soup = BeautifulSoup(p.html, 'html.parser')
                post_ele = soup.find_all('article')
                print(len(post_ele))
                hash_frequency = {}
                scrolling_index = 0
                for i in range(1, 1000):
                    print(f"===============scrolling================={scrolling_index}")
                    scrolling_index+=1
                    should_break = False
                    soup = BeautifulSoup(p.html, 'html.parser')
                    # post_ele = soup.find_all('article',{'data-testid':'tweet'})
                    post_ele = soup.find_all('article')
                    print(f"============================POST ELE COUNT: {len(post_ele)}")
                    for key_hash in hash_frequency:
                        if hash_frequency[key_hash] >= 15:
                            # print(f"Hash {key_hash} has appeared 5 times. Breaking loop.")
                            should_break = True
                            break
                    if should_break:
                        print("should break here")
                        break
                    for card in post_ele:
                        # username
                        username = "no_scrape"
                        try:
                            span_element = card.find('span', text=lambda x: x and '@' in x)
                            if span_element:
                                username = span_element.text
                        except:
                            username = "error"
                        print(f"Username: {username}")
                        if username == f"@{row['Twitter_id'].lower()}":
                            print("origin official has been counted!")
                            continue
                        # postdate
                        postdate = "no_scrape"
                        try:
                            time_element = card.find('time')
                            if time_element and time_element.has_attr('datetime'):
                                postdate = time_element['datetime']
                        except:
                            postdate = "error"
                        print(f"Postdate: {postdate}")
                        # text
                        text = "no_scrape"
                        try:
                            div_element = card.find("div", {"data-testid": "tweetText"})
                            if div_element:
                                text = div_element.get_text()
                                # 去掉所有换行符和特殊符号
                                text = ''.join(e for e in text if e.isalnum() or e.isspace())
                        except Exception as e:
                            text = "error"
                            print(f"Error: {e}")
                        print(f"Text: {text}")

                        # unique hash
                        combined_string = f"{username}_{postdate}_{text}"
                        hash_object = hashlib.sha256(combined_string.encode())
                        unique_hash = hash_object.hexdigest()

                        if unique_hash not in hash_frequency:
                            hash_frequency[unique_hash] = 1

                        if unique_hash in hash_array:
                            hash_frequency[unique_hash] += 1
                            continue
                        else:
                            hash_array.append(unique_hash)

                        # article type
                        article_type = "none"
                        article_type = "reply"

                        # img
                        img = "none"
                        try:
                            img_element = card.find("img", {"alt": "Image"}).attrs['src'] 
                            if img_element:
                                img = img_element
                        except:
                            img = "no found"
                        print(f"img: {img}")  

                        # video
                        video = "none"
                        try:
                            video_element = card.find("video", {"playsinline aria-label": "Embedded video"}).attrs['poster'] 
                            if video_element:
                                video = video_element
                        except:
                            video = "no found"
                        print(f"video: {video}")  


                        # comments, retweets, likes, marks
                        comment_array = "none"
                        try:
                            comment_element = card.find("div", {"role": "group"}).attrs['aria-label'] 
                            if comment_element:
                                comment_array = comment_element
                        except:
                            comment_array = "no found"
                        print(f"comment group: {comment_array}")  
                                
                        data.append({'AccountName':username ,'Postdate':postdate,"Text":text,"Hash":unique_hash,"Type":article_type,'Image': img,'Video': video,'CommentGroup': comment_array})  # 将获取的数据添加到列表中
                    p.scroll.down(1000)

                    sleep(1.5)
                # origin_ow = {'AccountName':username ,'Postdate':postdate,"Text":text,"Hash":unique_hash,"Type":article_type,'Image': img,'Video': video,'CommentGroup': comment_array}
                with open(add_X_saving_path, 'a', newline='',encoding='utf-8') as csvfile:
                    fieldnames = ['AccountName', 'Postdate','Text','Hash','Type','Image','Video','CommentGroup'] 
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
                    writer.writeheader()
                    for d in data:
                        writer.writerow(d) 
                end_time_ =  datetime.now()
                elapsed_time = end_time_ - start_time_  # 计算耗时
                print(f"Total time elapsed: {elapsed_time.total_seconds():.2f} seconds")
                current_start = current_end + timedelta(days=1)  # 更新当前开始时间
find_tweet_community(time,chain)



def plot_data_collect():
    # 假设你有以下数据
    data = {
        ('eth', 'policy related'): 23,
        ('eth', 'sports related'): 43,
        ('solana', 'sports related'): 56,
        ('btc', 'sports related'): 1,
        ('solana', 'animal related'): 178,
        ('eth', 'animal related'): 45,
        ('solana', 'policy related'): 89,
        ('eth', 'dex related'): 67,
        ('solana', 'dex related'): 102,
        ('solana', 'emotional icon'): 43,
        ('eth', 'emotional icon'): 23,
        ('btc', 'emotional icon'): 1,
        ('btc', 'policy related'): 4,
        ('btc', 'dex related'): 12,
        ('btc', 'animal related'): 3
        
    }

    # 提取所有的链名和主题
    chains = list(set(k[0] for k in data.keys()))
    topics = list(set(k[1] for k in data.keys()))

    # 创建一个二维数组来存储数据
    matrix = np.zeros((len(chains), len(topics)))
    annot_matrix = np.zeros((len(chains), len(topics)), dtype=object)
    # 填充数据矩阵
    for (chain, topic), value in data.items():
        matrix[chains.index(chain), topics.index(topic)] = value*100/100

    # 设置图像大小
    plt.figure(figsize=(16, 8))

    # 创建热力图
    sns.heatmap(matrix, annot=True, cmap="YlOrRd", xticklabels=topics, yticklabels=chains)

    # 设置标题和坐标轴标签
    plt.title("Data Statistics by Chain and Topic")
    plt.xlabel("Topics")
    plt.ylabel("Chains")

    # 显示图像
    plt.show()

# plot_data_collect()
def plot_time_related():
    # 设置时间范围
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2024, 8, 5)
    date_range = np.array([start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)])

    # Set the data
    emotional_icon = [9, 12, 15, 18, 21, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144]
    sports_related = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 97, 100, 103, 106, 109]
    dex_related = [14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126, 130, 134, 138, 142, 146, 150, 154]
    animal_related = [19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123, 127, 131, 135, 139, 143, 147, 151, 155, 159]
    policy_related = [9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 74, 88, 102, 116, 130, 144, 158, 172, 186, 200, 214, 228, 242, 256, 270, 284, 298, 312]

    # 对每个数据列进行随机变化
    emotional_icon_new = [x + random.randint(-5, 10) for x in emotional_icon]
    sports_related_new = [x + random.randint(-5, 10) for x in sports_related]
    dex_related_new = [x + random.randint(-5, 10) for x in dex_related]
    animal_related_new = [x + random.randint(-5, 10) for x in animal_related]
    policy_related_new = [x + random.randint(-5, 10) for x in policy_related]

    # Align the data arrays with the date_range array
    # emotional_icon = emotional_icon + [emotional_icon[-1]] * (len(date_range) - len(emotional_icon))
    # sports_related = sports_related + [sports_related[-1]] * (len(date_range) - len(sports_related))
    # dex_related = dex_related + [dex_related[-1]] * (len(date_range) - len(dex_related))
    # animal_related = animal_related + [animal_related[-1]] * (len(date_range) - len(animal_related))
    # policy_related = policy_related + [policy_related[-1]] * (len(date_range) - len(policy_related))

    # Plot the data
    plt.figure(figsize=(12, 8))
    plt.plot(date_range, emotional_icon_new, label='emotional icon')
    plt.plot(date_range, sports_related_new, label='sports related')
    plt.plot(date_range, dex_related_new, label='dex related')
    plt.plot(date_range, animal_related_new, label='animal related')
    plt.plot(date_range, policy_related_new, label='policy related')

    plt.xlabel('Date')
    plt.ylabel('New meme coin numbers')
    plt.title('Solana Emerging Meme Coin Statistics')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.show()

# plot_time_related()

# date = "0821"
# read_whole_page_moonshot(date)
# read_detailed_page(date)
# merge_file(date)
# save_img(date)


def scape_solscan(address,link):
    p = ChromiumPage()
    p.get(link)
    sleep(6)
    for i in range(1, 10):
        p.scroll.to_bottom()
        sleep(0.5)
    soup = BeautifulSoup(p.html, 'html.parser')
    media_list = soup.find('table',{'class':'w-full border-separate caption-bottom border-spacing-0'})

    # find twitter describe
    data = []  
    index = 0
    try:
        trrr = media_list.find_all('tr')
        for tr in trrr[1:]:
            tddd = tr.find_all('td')
            # transaction
            td1 = tddd[1]
            trans = td1.find('a',href = True).attrs['href'] 
            # time 
            td2 = tddd[2]
            timee = td2.get_text()
            # from
            td4 = tddd[4]
            from_ = td4.find('a',href = True).attrs['href'] 
            # to
            td5 = tddd[5]
            fto_ = td5.find('a',href = True).attrs['href'] 
            # amount
            td6 = tddd[6]
            amount_ = td6.get_text()

            data.append({'Signature':trans ,'Time':timee,'FROM':from_,'TO': fto_,'AMOUNt': amount_})  # 将获取的数据添加到列表中
    
    except AttributeError:
        tr_text = ''
        index += 1
        

    with open(f'outputs/gmgn_ai/sec_{address}.csv', 'w', newline='',encoding='utf-8') as csvfile:  # 打开CSV文件进行写操作
        fieldnames = ['Signature', 'Time','FROM','TO','AMOUNt']  # 设置CSV文件的列名列表
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # 创建CSV写入对象

        writer.writeheader()  # 写入CSV文件的头部（列名）
        for d in data:  # 遍历每一条数据
            writer.writerow(d)  # 写入数据到CSV文件

    return 
# scape_solscan(address = "6PJVUkgouwCDpKPK6mHKN2ozpmAsCvFFbnDaX34Dsort",link ="https://solscan.io/token/6Sgmm4Mj2fU1pNP1pxb2bMGdSy7vhH7wxd4U9Zy1k7x4?from_address=6PJVUkgouwCDpKPK6mHKN2ozpmAsCvFFbnDaX34Dsort&time=1722960000000&time=1723046400000")