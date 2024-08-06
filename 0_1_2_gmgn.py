from bs4 import BeautifulSoup  # 从bs4模块中导入BeautifulSoup类，用于解析HTML
import csv  # 导入csv模块，用于读写CSV文件
from selenium import __version__
from DrissionPage import ChromiumPage
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
def read_whole_page(chain,address_page,symbol):
    p = ChromiumPage()
    p.get(f'https://gmgn.ai/{chain}/token/{address_page}?symbol={symbol}')
    print(f'https://gmgn.ai/{chain}/token/{address_page}?symbol={symbol}')
    sleep(60)

    soup = BeautifulSoup(p.html, 'html.parser')
    tabel= soup.find('tbody',{'class':'g-table-tbody'})

    row_herfs = tabel.find_all('tr')
    num_rows = len(row_herfs)
    print("Number of rows:", num_rows)
    data = []  # 创建一个空列表，用于存储解析后的数据
    for row in row_herfs:  # 遍历每一行
        text_array = []
        # find all data
        all_table_cell = row.find_all('td',{'class':'g-table-cell'})
        print("length of td: ",len(all_table_cell))
        address = ""
        for elem in all_table_cell:  
            try:
                # find address link
                address_link = elem.find('a',  attrs={'class': "css-zaq9jo"},href = True).attrs['href']
                address = address_link.split('/')[-1]
            except AttributeError:
                print("skip")
            text_array.append(elem.get_text())
        data.append({"Text_List":text_array,"Address":address})
        print(text_array) 

    with open(f'outputs/gmgn_ai/{chain}_{address_page}_{symbol}.csv', 'w', newline='',encoding='utf-8') as csvfile:  # 打开CSV文件进行写操作
        writer = csv.DictWriter(csvfile, fieldnames=['Text_List','Address'])
        writer.writeheader()  # 写入字段名

        for d in data:
            writer.writerow(d)
    p.quit()

# read_whole_page("sol","Hc87jMpH7yb8snpdkSh4LwTEiehW3ubE7QpSwS3epump","SMILE")

def file_refine(chain,address_page,symbol):
    with open(f'outputs/gmgn_ai/{chain}_{address_page}_{symbol}.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    new_rows = []
    for row in rows[1:]:
        if row:
            text_list = eval(row[0])
            address = row[1]
            time = text_list[0]
            action = text_list[1]
            dollar = text_list[2]
            if isinstance(dollar, str) and dollar.startswith('$'):
                dollar = dollar[1:] 
            amount = text_list[3]
            if isinstance(amount, str):
                amount = amount[:-1] 
            price = text_list[4]
            if isinstance(price, str) and price.startswith('$'):
                price = price[1:] 
            new_row = [time, action, dollar, amount, price, address]
            new_rows.append(new_row)

    with open(f'outputs/gmgn_ai/_{chain}_{address_page}_{symbol}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Action', 'Dollar', 'Amount', 'Price', 'Address'])
        writer.writerows(new_rows)
# file_refine("sol","Hc87jMpH7yb8snpdkSh4LwTEiehW3ubE7QpSwS3epump","SMILE")

def plot_transfer(chain,address_page,symbol):
    # 读取 CSV 文件
    file_path = f'outputs/gmgn_ai/_{chain}_{address_page}_{symbol}.csv' 
    data = pd.read_csv(file_path)
    data = data[data['Address'] == "57od7783D4GeCkmnuzewjK3R6oFpffNMhQscisnu9vfE"]

    # 假设 CSV 文件中有 'time' 和 'dollar' 两列
    # 确保时间列被解析为 datetime 格式
    data['Time'] = pd.to_datetime(data['Time'], format='%d/%m %H:%M:%S')

    # 将 dollar 列转换为数值类型 (如果 dollar 列有 $ 符号，先去掉 $)
    data['Dollar'] = data['Dollar'].str.replace(',', '').astype(float)

    plt.figure(figsize=(12, 6))
    plt.plot(data['Time'], data['Dollar'], marker='o', linestyle='-', color='b')

    # 添加标题和标签
    plt.title('Dollar Over Time')
    plt.xlabel('Time')
    plt.ylabel('Dollar')

    # 显示网格
    plt.grid()

    # 显示图表
    plt.xticks(rotation=45)  # 使 x 轴标签倾斜以便更好阅读
    plt.tight_layout()  # 自动调整布局以防止标签重叠
    plt.savefig(f'outputs/gmgn_ai/_{chain}_{address_page}_{symbol}.png' )
plot_transfer("sol","Hc87jMpH7yb8snpdkSh4LwTEiehW3ubE7QpSwS3epump","SMILE")