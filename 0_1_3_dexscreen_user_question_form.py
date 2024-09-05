import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def draw_questionnar_result():
    # 读取CSV文件
    df = pd.read_csv('outputs/dex_scrape/user_questioning/topic_collection_list.csv', header=None, names=['Name', 'ID', 'Category', 'Method', 'Sentiment', 'Safety'])

    # 创建三个透视表
    pivot_method = df.pivot_table(index='Category', columns='Method', aggfunc='size', fill_value=0)
    pivot_sentiment = df.pivot_table(index='Category', columns='Sentiment', aggfunc='size', fill_value=0)
    pivot_safety = df.pivot_table(index='Category', columns='Safety', aggfunc='size', fill_value=0)

    # 合并透视表
    merged_df = pd.concat([pivot_method, pivot_sentiment, pivot_safety], axis=1)

    # 绘制表格
    plt.figure(figsize=(18, 8))
    sns.heatmap(merged_df, annot=True, cmap='YlGnBu', fmt='d', linewidths=.5)
    plt.title('Data Summary')
    plt.show()




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