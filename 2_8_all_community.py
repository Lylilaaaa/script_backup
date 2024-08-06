import networkx as nx
import community as comm
import matplotlib.pyplot as plt
import os

def community_detection(file_name):
    # 读取边缘列表文件，创建一个无向图
    G = nx.read_edgelist(file_name, delimiter=',', create_using=nx.Graph(), nodetype=str, data=False)
    
    # 使用 Louvain 方法进行社区划分
    partition = comm.best_partition(G)
    
    # 统计每个社区的节点数量
    community_sizes = {}
    for node, community_id in partition.items():
        if community_id not in community_sizes:
            community_sizes[community_id] = 0
        community_sizes[community_id] += 1
    
    # 绘制饼状图
    sizes = list(community_sizes.values())
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f"Community distribution for {os.path.basename(file_name)}")
    plt.savefig(f"community_distribution_{os.path.basename(file_name)}.png")
    plt.show()

# 文件名列表
edge_files = ["tweet/outputs/Pepe/Pepe_edge.csv", "tweet/outputs/BALD/BALD_edge.csv", "tweet/outputs/SLERF[no_trans]/SLERF_edge.csv", "tweet/outputs/ConstitutionDAO_edge.csv"]

# 对每个边缘列表文件进行社区划分分析
for file_name in edge_files:
    community_detection(file_name)
