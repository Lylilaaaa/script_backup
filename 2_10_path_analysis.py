import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 读取所有csv文件并创建图
# edge_files = ["tweet/outputs/Pepe/Pepe_edge.csv", "tweet/outputs/BALD/BALD_edge.csv", "tweet/outputs/SLERF[no_trans]/SLERF_edge.csv", "tweet/outputs/ConstitutionDAO_edge.csv"]
edge_files = ["tweet/outputs/ConstitutionDAO_edge.csv"]
graphs = []
result_df = pd.DataFrame(columns=['Graph', 'Source', 'Target', 'ShortestPath'])
for file_name in edge_files:
    df = pd.read_csv(file_name)
    G = nx.from_pandas_edgelist(df, 'src', 'dst', create_using=nx.DiGraph())
    graphs.append((file_name, G))

# 在每个图中进行路径传播检测
for file_name, G in graphs:
    print(f"Path propagation analysis for {file_name}:")
    for source_node in G.nodes():
        for target_node in G.nodes():
            if source_node != target_node:
                try:
                    shortest_path = nx.shortest_path(G, source=source_node, target=target_node)
                    result_df = result_df._append({'Graph': file_name, 'Source': source_node, 'Target': target_node, 'ShortestPath': shortest_path}, ignore_index=True)
                except nx.NetworkXNoPath:
                    pass
result_df.to_csv("tweet/outputs/ConstitutionDAO_path_propagation_analysis.csv", index=False)