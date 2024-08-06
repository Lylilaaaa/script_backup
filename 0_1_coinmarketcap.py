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
# options= Options() 

# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.get('https://coinmarketcap.com/view/memes/?page=1')

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

# 使用driver访问网站
driver.get('https://coinmarketcap.com/view/memes/?page=24')



page_height=driver.execute_script("return document.body.scrollHeight;")

for i in range(1,31):
    scroll_s=str((i-1)*page_height/30)
    scroll_e=str(i*page_height/30)
    js = 'window.scrollTo('+scroll_s + ','+scroll_e+')'
    driver.execute_script(js)
    time.sleep(2)


soup = BeautifulSoup(driver.page_source, 'html.parser')

table = soup.find('table', {'class': 'cmc-table'})  # 查找表格元素
tbody = table.find('tbody')  # 查找表格内容的 <tbody> 标签
rows = tbody.find_all('tr')  # 查找所有的行 <tr> 标签
num_rows = len(rows)
print("Number of rows:", num_rows)
data = []  # 创建一个空列表，用于存储解析后的数据
for row in rows:  # 遍历每一行
    try:
        div_b = row.find('div', {'class': "sc-4c05d6ef-0 bLqliP"}) 
        link_elem = div_b.find('a',  attrs={'class': "cmc-link"},href = True).attrs['href']  # 获取货币link
        link = link_elem
    except AttributeError:
        symbol = ''
    try:
        symbol_elem = row.find('p', {'class': "sc-71024e3e-0 OqPKt coin-item-symbol"}).text.strip()  # 获取货币大写缩写
        symbol = symbol_elem
    except AttributeError:
        symbol = ''

    try:
        name_elem = row.find('p', {'class': 'sc-71024e3e-0 ehyBa-d'}).text.strip()  # 获取货币名称 小写
        name = name_elem
    except AttributeError:
        name = ''
    data.append({'Symbol': symbol, 'Name': name,'Link': link})  # 将获取的数据添加到列表中

with open('outputs/sec_scrape/coinmarketcap_page24.csv', 'w', newline='',encoding='utf-8') as csvfile:  # 打开CSV文件进行写操作
    fieldnames = ['Symbol', 'Name','Link']  # 设置CSV文件的列名列表
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # 创建CSV写入对象

    writer.writeheader()  # 写入CSV文件的头部（列名）
    for d in data:  # 遍历每一条数据
        writer.writerow(d)  # 写入数据到CSV文件

data = driver.page_source
driver.quit()