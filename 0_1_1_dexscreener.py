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
import re
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

def read_whole_page(time):
    p = ChromiumPage()
    p.get('https://dexscreener.com/moonshot')
    sleep(5)

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



def read_detailed_page(time):
    # read data file
    date_list_path = f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/dex_scrape_moonshot_{time}.csv"
    date_df = pd.read_csv(date_list_path)
    data = []
    link_list = date_df['Link'].tolist()
    for _link in link_list:
        p = ChromiumPage()
        p.get(f'https://dexscreener.com{_link}')
        sleep(5)
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
    with open(f'outputs/dex_scrape/dex_scrape_moonshot_{time}_detailed.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Link', 'Total_Describe', 'Price', 'Price_Percentage', 'Volume', 'Attitude', 'Social_Links']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in data:
            writer.writerow(d)

        p.quit()



def merge_file(time):
    csv_file1 = f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/dex_scrape_moonshot_{time}_detailed.csv"
    csv_file2 = f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/dex_scrape_moonshot_{time}.csv"

    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    merged_df = pd.merge(df1, df2, on='Link', how='outer')

    output_file = f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/dex_scrape_moonshot_{time}_merge.csv"
    merged_df.to_csv(output_file, index=False)


def save_img(time):
    csv_file = f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/dex_scrape_moonshot_{time}_merge.csv"
    df = pd.read_csv(csv_file)
    base_dir = f"D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/images/{time}"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    total_images = len(df)
    for index, row in tqdm(df.iterrows(), total=total_images, unit="image", desc="Downloading images"):
        img_link = row['Img_link']
        link = row['Link']

        soup = BeautifulSoup(img_link, 'html.parser')
        img_tag = soup.find('img')
        img_link = img_tag['src'] if img_tag else None

        print(img_link)
        file_name = os.path.splitext(link.split('/')[-1])[0]
        img_path = os.path.join(base_dir, file_name)
        response = requests.get(img_link)
        with open(img_path, 'wb') as file:
            file.write(response.content)

        print(f"Image saved: {img_path}")
        sleep(2)

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

def scape_tweet(address,tweet_id,link):
    p = ChromiumPage()
    p.get(link)
    sleep(10)
    soup = BeautifulSoup(p.html, 'html.parser')
    if "This account doesn’t exist" in soup.get_text() or "This account doesn't exist" in soup.get_text():
        print(f"{address}")
        p.quit()
        return
    p.get(f"{link}/media")
    sleep(10)
    p.scroll.to_bottom()
    sleep(10)
    soup = BeautifulSoup(p.html, 'html.parser')
    media_list = soup.find_all('li',{'role':'listitem'})

    num_rows = len(media_list)

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

    with open(f'outputs/dex_scrape/tweet/dex_scrape_tweet_{address}.csv', 'w', newline='',encoding='utf-8') as csvfile:  # 打开CSV文件进行写操作
        fieldnames = ['Address', 'Tweet','Img_index','Img_link','Img']  # 设置CSV文件的列名列表
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # 创建CSV写入对象

        writer.writeheader() 
        for d in data: 
            writer.writerow(d) 
    p.quit()

def start_scrape():
    meme_list_df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/merge/info_image_merge_twitter.csv")
    link_list = meme_list_df['Twitter_link'] 
    id_list = meme_list_df['Twitter_id'] 
    address_list = meme_list_df['Address'] 
    for i, ele in enumerate(link_list):
        scape_tweet(address_list[i],id_list[i],ele)
start_scrape()

def get_twitter_list():
    meme_list_df = pd.read_csv("D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/merge/info_image_merge_twitter.csv")
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
    meme_list_df.to_csv("D:/Research_PostGraduate/web3/tweet/outputs/dex_scrape/merge/info_image_merge_twitter.csv", index=False)
# get_twitter_list()


# date = "0806"
# read_whole_page(date)
# read_detailed_page(date)
# merge_file(date)
# save_img(date)