import networkx as nx
import matplotlib.pyplot as plt

def isolate_subgraph_anomaly_detection(G):
    isolated_subgraphs = []
    threshold = 0.3  # 调整判断异常节点的阈值
    
    for node in G.nodes():
        neighbors = set(G.neighbors(node))
        is_anomaly = True
        
        for other_node in G.nodes():
            if other_node != node:
                other_neighbors = set(G.neighbors(other_node))
                overlap = len(neighbors.intersection(other_neighbors)) / min(len(neighbors), len(other_neighbors))
                if overlap > threshold:  # 调整判断异常节点的条件
                    is_anomaly = False
                    break
        
        if is_anomaly:
            isolated_subgraphs.append(G.subgraph([node] + list(neighbors)))
    
    return isolated_subgraphs

# 文件名
file_name = "tweet/outputs/SLERF[no_trans]/SLERF_edge.csv"

# 读取边缘列表文件，创建一个无向图
G = nx.read_edgelist(file_name, delimiter=',', create_using=nx.Graph(), nodetype=str, data=False)

# 孤立子图异常检测
isolated_subgraphs = isolate_subgraph_anomaly_detection(G)

# 绘制孤立子图
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, node_color='skyblue', node_size=300, font_size=10)
for subgraph in isolated_subgraphs:
    nx.draw_networkx_edges(G, pos, edgelist=subgraph.edges(), width=2, edge_color='r', alpha=0.5)
plt.title("Isolate Subgraph Anomaly Detection")
plt.show()

# 获取总边数
total_edges = G.number_of_edges()

# 获取异常边的数量
anomalous_edges = sum(subgraph.number_of_edges() for subgraph in isolated_subgraphs)

# 计算异常边的占比
anomalous_edge_ratio = (anomalous_edges / total_edges) * 100

print("Total edges:", total_edges)
print("Anomalous edges:", anomalous_edges)
print("Anomalous edge ratio:", anomalous_edge_ratio, "%")