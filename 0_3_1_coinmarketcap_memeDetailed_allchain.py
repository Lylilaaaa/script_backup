import requests  # 导入requests库，用于发送HTTP请求
from bs4 import BeautifulSoup  # 从bs4模块中导入BeautifulSoup类，用于解析HTML
import csv  # 导入csv模块，用于读写CSV文件

import requests  # 导入requests库，用于发送HTTP请求
from bs4 import BeautifulSoup  # 从bs4模块中导入BeautifulSoup类，用于解析HTML
import csv  # 导入csv模块，用于读写CSV文件
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import time
import pandas as pd
from tqdm import tqdm
import pandas as pd

def init_driver(headless=True, proxy="http://127.0.0.1:7890", option=None):
    """ initiate a chromedriver or firefoxdriver instance
        --option : other option to add (str)
    """

    options = Options()
    driver_path = ChromeDriverManager().install()

    if headless is True:
        print("Scraping on headless mode.")
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False
    options.add_argument('log-level=3')
    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
        print("using proxy : ", proxy)
    if option is not None:
        options.add_argument(option)

    driver = webdriver.Chrome(service=Service(driver_path), options=options)  # 修改此行以添加代理

    return driver

driver = init_driver(proxy="http://127.0.0.1:7890")


base_url = "https://coinmarketcap.com/currencies/"
df = pd.read_csv('outputs/sec_scrape/coinmarketcap_page_merge.csv', encoding='latin-1')

coinList = df['web_name']

# coinList = ['dogecoin','shiba-inu','pepe','dogwifhat','floki-inu','bonk1','book-of-meme','meme','based-brett','degen-base','mew','baby-doge-coin','coq-inu','wen','myro','mog-coin','slerf','toshithecat','maga','bone-shibaswap','smog','dogelon','tokenfi','erc20','milady-meme-coin','pepefork','harrypotterobamasonic10inu-eth','snek']
# coinList2 = ['grok-erc','arbdoge-ai','doge-killer','richquack-com','kishu-inu','turbo','samoyedcoin','katana-inu','pitbull','duko','dejitaru-tsuka','volt-inu-v2']
# coinList.extend(coinList2)
data = []  # 创建一个空列表，用于存储解析后的数据

def get_coin_data(coinName):
    url = base_url + coinName + "/"
    driver.get(url)
    time.sleep(2)
    # response = requests.get(url)  # 发送GET请求获取网页内容
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # 解析HTML内容
    try:
        chain_elem = soup.find('span', {'class': "sc-71024e3e-0 dEZnuB"}).text.strip()  # chain_id
        chain = chain_elem
    except AttributeError:
        print(coinName)
        chain = ''

    try:
        add_elem = soup.find('a', attrs={'class': "chain-name"}, href=True).attrs['href']  # address
        address = add_elem
    except AttributeError:
        print(coinName)
        address = ''
    try:
        link_elem = soup.find_all('div', attrs={'class': "sc-d1ede7e3-0 sc-7f0f401-0 gRSwoF gQoblf"})  # social
        links = ''
        for li in link_elem:
            try:
                get_link = li.find('a', attrs={'rel': 'nofollow noopener'}, href=True).attrs['href']
                link_name = li.find('a', attrs={'rel': 'nofollow noopener'}).text.strip()
                link_pair = f"{link_name}: {get_link}"
                links += link_pair
            except AttributeError:
                print(coinName)
                links += ''
    except AttributeError:
        print(coinName)
        links += ''

    


    return {'Name': coinName, 'Chain': chain, 'Address': address, 'Social': links}



for i, coinName in enumerate(tqdm(coinList, desc="Processing coins", unit="coin")):

    # if i < 100:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 99:
    #         file_path = 'coinmarketcap_1.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # if 100 <= i < 200:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 199:
    #         file_path = 'coinmarketcap_2.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 200 <= i < 300:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 299:
    #         file_path = 'coinmarketcap_3.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 300 <= i < 400:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 399:
    #         file_path = 'coinmarketcap_4.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # if 400 <= i < 500:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 499:
    #         file_path = 'coinmarketcap_5.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 500 <= i < 600:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 599:
    #         file_path = 'coinmarketcap_6.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 600 <= i < 700:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 699:
    #         file_path = 'coinmarketcap_7.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 700 <= i < 800:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 799:
    #         file_path = 'coinmarketcap_8.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 800 <= i < 900:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 899:
    #         file_path = 'coinmarketcap_9.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 900 <= i < 1000:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 999:
    #         file_path = 'coinmarketcap_10.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # if 1000 <= i < 1100:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1099:
    #         file_path = 'coinmarketcap_11.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 1100 <= i < 1200:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1199:
    #         file_path = 'coinmarketcap_12.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # if 1200 <= i < 1300:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1299:
    #         file_path = 'coinmarketcap_13.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 1300 <= i < 1400:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1399:
    #         file_path = 'coinmarketcap_14.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 1400 <= i < 1500:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1499:
    #         file_path = 'coinmarketcap_15.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 1500 <= i < 1600:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1599:
    #         file_path = 'coinmarketcap_16.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 1600 <= i < 1700:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1699:
    #         file_path = 'coinmarketcap_17.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 1700 <= i < 1800:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1799:
    #         file_path = 'coinmarketcap_18.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 1800 <= i < 1900:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1899:
    #         file_path = 'coinmarketcap_19.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []
    # elif 1900 <= i < 2000:
    #     coin_data = get_coin_data(coinName)
    #     data.append(coin_data)
    #     if i == 1999:
    #         file_path = 'coinmarketcap_20.csv'
    #         df = pd.DataFrame(data)
    #         df.to_csv(file_path, index=False)
    #         data = []       
    if 2000 <= i < 2100:
        coin_data = get_coin_data(coinName)
        data.append(coin_data)
        if i == 1999:
            file_path = 'coinmarketcap_21.csv'
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            data = []        
    elif 2100 <= i < 2200:
        coin_data = get_coin_data(coinName)
        data.append(coin_data)
        if i == 1999:
            file_path = 'coinmarketcap_22.csv'
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            data = []    
    elif 2200 <= i < 2300:
        coin_data = get_coin_data(coinName)
        data.append(coin_data)
        if i == 1999:
            file_path = 'coinmarketcap_23.csv'
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            data = []   
    elif 2300 <= i < 2400:
        coin_data = get_coin_data(coinName)
        data.append(coin_data)
        if i == 1999:
            file_path = 'coinmarketcap_24.csv'
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            data = []  
# with open('coinmarketcap.csv', 'w', newline='', encoding='utf-8') as csvfile:  # 打开CSV文件进行写操作
#     fieldnames = ['Name', 'Market','Chain','Address','Social']  # 设置CSV文件的列名列表
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # 创建CSV写入对象

#     writer.writeheader()  # 写入CSV文件的头部（列名）
#     for d in data:  # 遍历每一条数据
#         try:
#             writer.writerow(d)  # 写入数据到CSV文件
#         except AttributeError:
                # print("error")