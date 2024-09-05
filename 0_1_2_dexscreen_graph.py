import pandas as pd
import networkx as nx
import ast
import re
from pandas import Timestamp

def parse_timestamp_dict(timestamp_str):
    """将包含 Timestamp 的字符串转换为字典"""
    timestamp_dict = {}
    # print(timestamp_str)
    # 使用正则表达式提取时间戳和对应的值
    pattern = re.compile(r"Timestamp\('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{4})', tz='UTC'\): (\d+\.\d+)")
    matches = re.findall(pattern, timestamp_str)
    for match in matches:
        timestamp_dict[Timestamp(match[0])] = float(match[1])
    # print(timestamp_dict)
    return timestamp_dict





def filter_nodes_by_text_sentiment(node_df):
    """过滤掉 text_sentiment 中所有对应数值均为 0 的行"""
    def has_non_zero_sentiment(text_sentiment_str):
        text_sentiment = parse_timestamp_dict(text_sentiment_str)
        return any(value != 0 for value in text_sentiment.values())
    print("orgin line: ",len(node_df))
    # 过滤掉 text_sentiment 中所有对应数值均为 0 的行   "{Timestamp('2024-08-14 23:26:16+0000', tz='UTC'): 1.0, Timestamp('2024-08-15 08:30:54+0000', tz='UTC'): 0.4333333333333333}"
    filtered_df = node_df[node_df['text_sentiment'].apply(has_non_zero_sentiment)]
    print("after line: ",len(filtered_df))
    return filtered_df



def form_gexf_file():
    # 读取 edge.csv 文件
    edge_df = pd.read_csv('outputs/graph_csv_outputs/edges.csv')

    # 读取 node.csv 文件
    node_df = pd.read_csv('outputs/graph_csv_outputs/nodes.csv')
    node_df = filter_nodes_by_text_sentiment(node_df)

    address_dict = {}
    address_counter = 1
    def get_address_type(addresses):
        nonlocal address_counter
        addresses_set = set(ast.literal_eval(addresses))
        num_addresses = len(addresses_set)
        if num_addresses == 1:
            unique_address = list(addresses_set)[0]
            if unique_address not in address_dict:
                address_dict[unique_address] = address_counter
                address_counter += 1
            return address_dict[unique_address]

        else:
            return 43 + num_addresses  # 返回 44, 45, 46, 等等
        
    node_df['address_type'] = node_df['addr'].apply(get_address_type)
    node_df.to_csv('outputs/graph_csv_outputs/nodes_.csv')
    # node_df['tweetid']   = node_df['tweetid'].apply(lambda x: {extract_tweetid(tid) for tid in ast.literal_eval(x)})
    # node_df.to_csv('outputs/graph_csv_outputs/nodes.csv')

    G = nx.DiGraph()

    # 添加边到图中
    for index, row in edge_df.iterrows():
        source = row['source']
        target = row['target']
        attributes = ast.literal_eval(row['attributes'])  # 将字符串转换为字典
        G.add_edge(source, target, **attributes)

    # 添加节点到图中
    for index, row in node_df.iterrows():
        node = row['node']
        addr = str(list(ast.literal_eval(row['addr'])))  # 将字符串转换为集合并转换为列表
        account_name = str(row['account_name'])
        tweetid = str(list(row['tweetid']))  # 已经处理过的 tweetid
        address_type = row['address_type']
        # Postdate = str(parse_timestamp_dict(row['Postdate']))  # 将字符串转换为字典并转换为字符串
        text_sentiment = parse_timestamp_dict(row['text_sentiment']) 
        text_sentiment_str = str(text_sentiment)  # 将字符串转换为字典并转换为字符串
        
        avg_sentiment = sum(text_sentiment.values()) / len(text_sentiment) if text_sentiment else 0
        # 添加节点及其属性
        G.add_node(node, addr=addr, account_name=account_name, tweetid=tweetid, text_sentiment=text_sentiment_str, avg_sentiment=avg_sentiment,address_type = address_type)

    # 将图保存为 GEXF 文件
    nx.write_gexf(G, 'graph.gexf')

    print("GEXF 文件已成功生成！")

def teat_re():
    timestamp_str = "{Timestamp('2024-08-22 11:22:06+0000', tz='UTC'): 0.0, Timestamp('2024-08-23 12:34:56+0000', tz='UTC'): 1.0}"

    pattern = re.compile(r"Timestamp\('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{4})', tz='UTC'\): (\d+\.\d+)")

    matches = pattern.findall(timestamp_str)

    for match in matches:
        timestamp, value = match
        print(f"Timestamp: {timestamp}, Value: {value}")

if __name__ == "__main__":
    form_gexf_file()
    # teat_re()
