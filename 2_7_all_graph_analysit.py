import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd
def load_and_visualize_graph(file_name, output_file,tile):
    # 读取边缘列表文件，创建一个无向图
    df = pd.read_csv(file_name)
    # G = nx.read_edgelist(file_name, delimiter=',', create_using=nx.Graph(), nodetype=str, data=False)
    G = nx.from_pandas_edgelist(df, source='From', target='To', create_using=nx.DiGraph())
    # 计算网络中的各种中心性指标
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    
    # 绘制中心性指标的频率柱状图
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 3, 1)
    plt.hist(degree_centrality.values(), bins=20, color='skyblue')
    plt.title('Degree Centrality')
    plt.xlabel('Degree Centrality')
    plt.ylabel('Frequency')
    plt.yscale('log')

    plt.subplot(1, 3, 2)
    plt.hist(betweenness_centrality.values(), bins=20, color='lightgreen')
    plt.title('Betweenness Centrality')
    plt.xlabel('Betweenness Centrality')
    plt.ylabel('Frequency')
    plt.yscale('log')

    plt.subplot(1, 3, 3)
    plt.hist(closeness_centrality.values(), bins=20, color='salmon')
    plt.title('Closeness Centrality')
    plt.xlabel('Closeness Centrality')
    plt.ylabel('Frequency')
    plt.suptitle(tile)

    plt.tight_layout()
    
    # 保存频率图
    plt.savefig(output_file)
    
    # 显示频率图
    plt.show()

# 文件名列表
edge_files = ["tweet/outputs/Pepe/export-token-0x6982508145454ce325ddbe47a25d4ec3d2311933.csv","tweet/outputs/BALD/export-token-0x27d2decb4bfc9c76f0309b8e88dec3a601fe25a8.csv",  "tweet/outputs/export-token-0x7a58c0be72be218b41c608b7fe7c5bb630736c71.csv"]
output_files = ["tweet/outputs/Pepe/Pepe_trans.png","tweet/outputs/BALD/BALD_trans.png", "tweet/outputs/ConstitutionDAO_trans.png"]
name = ['Pepe','BALD','ConstitutionDAO']
# 对每个边缘列表文件进行加载和可视化s
for file_name, output_file,name_ in zip(edge_files, output_files,name):
    load_and_visualize_graph(file_name, output_file,name_)