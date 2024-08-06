import json
from datetime import datetime, timedelta
from tqdm import tqdm
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
    # for file in tqdm(file_list, desc="Processing unique topics"):
    #     if file.endswith(".csv"):
    #         coin_name = os.path.splitext(file)[0]
    #         if coin_name.endswith("_clean"):
    #             os.remove(os.path.join(new_directory, file))
    #             print(f"Deleted {file}")
def edge_data_reframe(df):
    
    dfs = []
    for index, row in df.iterrows():
        # time = row['date']
        from_ = row['topic1']
        to_ = row['topic2']
        # event_ = row['event_txt']
        data = {'src': from_, 'dst': to_}
        dfs.append(data)
        merged_df = pd.DataFrame(dfs)
    return merged_df
    
import networkx as nx
import itertools
from collections import Counter


def find_frequent_patterns(graph):
    triple_patterns = Counter()
    quad_patterns = Counter()
    for node in graph.nodes():
        neighbors = list(graph.successors(node))
        for triple in itertools.combinations(neighbors, 2):
            triple = tuple(sorted([node] + list(triple)))
            triple_patterns[triple] += 1
        for quad in itertools.combinations(neighbors, 3):
            quad = tuple(sorted([node] + list(quad)))
            quad_patterns[quad] += 1
    most_common_triple = triple_patterns.most_common(1)
    most_common_quad = quad_patterns.most_common(1)
    
    return most_common_triple, most_common_quad


def terminate_find_graphlet():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/rug_pull_not_comfirm"
    eth_csv_path = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    eth_df = pd.read_csv(eth_csv_path)
    for root, dirs, files in tqdm(os.walk(new_directory), desc="Processing unique topics"):
        for file in files:
            if file.endswith(".csv"):
                coin_name = os.path.splitext(file)[0]
                if coin_name.endswith("_clean"):
                    coin_name = coin_name[:-6]
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path, low_memory=False)
    G = nx.from_pandas_edgelist(df, 'src', 'dst', create_using=nx.Graph())
    most_common_triple, most_common_quad = find_frequent_patterns(G)

    print("Most frequent triple pattern:", most_common_triple)
    print("Most frequent quad pattern:", most_common_quad)


def calculate_degree_distribution(df):
    # print(len(list(df)))
    G = nx.from_pandas_edgelist(df, 'src', 'dst', create_using=nx.DiGraph())
    degree_distribution = nx.degree_histogram(G)
    degrees = range(1, len(degree_distribution) + 1)
    nonzero_indices = [i for i, val in enumerate(degree_distribution) if val != 0]
    nonzero_degrees = [degrees[i] for i in nonzero_indices]
    nonzero_distribution = [degree_distribution[i] for i in nonzero_indices]
    log_nonzero_degrees = np.log(nonzero_degrees)
    log_nonzero_distribution = np.log(nonzero_distribution)
    coefficients = np.polyfit(log_nonzero_degrees, log_nonzero_distribution, 1)
    poly = np.poly1d(coefficients)
    lambda_value = -coefficients[0]

    try:
        eigenvector_centrality = nx.eigenvector_centrality(G)
        e_centrality_values = list(eigenvector_centrality.values())
        print("Finish eigenvector_centrality")
    except:
        e_centrality_values = None

    betweenness_centrality = nx.betweenness_centrality(G)
    b_centrality_values = list(betweenness_centrality.values())
    print("Finish betweenness_centrality")

    closeness_centrality = nx.closeness_centrality(G)
    c_centrality_values = list(closeness_centrality.values())
    print("Finish closeness_centrality")

    return log_nonzero_degrees,log_nonzero_distribution,poly,lambda_value,e_centrality_values,b_centrality_values,c_centrality_values
    # degrees = [val for (node, val) in G.degree()]
    # degree_freq = np.bincount(degrees)
    # degree_freq = degree_freq[1:]
    # log_degree = np.log(range(1, len(degree_freq)+1))
    # log_freq = np.log(degree_freq)
    # try:
    #     coeffs = np.polyfit(log_degree, log_freq, 1)
    #     alpha = -coeffs[0]
    #     return log_degree, log_freq, alpha
    # except:
    #     return None, None, None


def process_data_and_generate_images():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/rug_pull_not_comfirm"
    eth_csv_path = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"

    eth_df = pd.read_csv(eth_csv_path)

    for root, dirs, files in tqdm(os.walk(new_directory), desc="Processing unique topics"):
        for file in files:
            if file.endswith(".csv"):
                coin_name = os.path.splitext(file)[0]
                if coin_name.endswith("_clean"):
                    coin_name = coin_name[:-6]
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path, low_memory=False)
                    df['date'] = pd.to_datetime(df['date'])
                    graph_df = edge_data_reframe(df)
                    log_nonzero_degrees, log_nonzero_distribution, poly, lambda_value, e_v, b_v, c_v = calculate_degree_distribution(graph_df)

                    save_degree_path = f"{new_directory}/{coin_name}/{coin_name}_degree.png"
                    plt.scatter(log_nonzero_degrees, log_nonzero_distribution, alpha=0.7, s=10)
                    plt.plot(log_nonzero_degrees, poly(log_nonzero_degrees), color='red', label='Fitted Line')
                    plt.xlabel('Degree(log)')
                    plt.ylabel('Frequency(log)')
                    plt.title(f'Degree Distribution of {coin_name} Degree: {lambda_value}')
                    plt.savefig(save_degree_path)
                    plt.close()

                    centrality_data = {"Eigenvector Centrality": e_v, "Closeness Centrality": b_v, "Betweenness Centrality": c_v}
                    for centrality_name, centrality_values in centrality_data.items():
                        save_centrality_path = f"{new_directory}/{coin_name}/{coin_name}_{centrality_name.lower().replace(' ', '_')}.png"
                        centrality_values_counts = {}
                        for value in centrality_values:
                            centrality_values_counts[value] = centrality_values_counts.get(value, 0) + 1
                        max_frequency_value = max(centrality_values_counts, key=centrality_values_counts.get)
                        max_frequency = centrality_values_counts[max_frequency_value]
                        x = list(centrality_values_counts.keys())
                        y = list(centrality_values_counts.values())
                        x_log = [np.log10(val) for val in x]
                        y_log = [np.log10(val) for val in y]
                        plt.scatter(x_log, y_log, alpha=0.7)
                        plt.xlabel(f'{centrality_name}')
                        plt.ylabel('Frequency')
                        plt.title(f'{centrality_name} Distribution of {coin_name}')
                        plt.savefig(save_centrality_path)
                        plt.close()
                        eth_df.loc[eth_df["Name"] == coin_name, centrality_name] = f"{max_frequency},{max_frequency_value}"

                    eth_df.loc[eth_df["Name"] == coin_name, "degree_lambda"] = lambda_value

    eth_df.to_csv(eth_csv_path, index=False)

#process_data_and_generate_images()

def process_single_folder_directory(new_directory, eth_csv_path):
    eth_df = pd.read_csv(eth_csv_path)
    half_length = len(os.listdir(new_directory)) // 2
    for file in tqdm(os.listdir(new_directory)[half_length:], desc="Processing unique topics"):
        if file.endswith(".csv"):
            coin_name = os.path.splitext(file)[0]
            if coin_name.endswith("_clean"):
                coin_name = coin_name[:-6]
                file_path = os.path.join(new_directory, file)
                df = pd.read_csv(file_path, low_memory=False)
                df['date'] = pd.to_datetime(df['date'])
                graph_df = edge_data_reframe(df)
                log_nonzero_degrees, log_nonzero_distribution, poly, lambda_value, e_v, b_v, c_v = calculate_degree_distribution(graph_df)

                save_degree_path = f"{new_directory}/{coin_name}_degree.png"
                plt.scatter(log_nonzero_degrees, log_nonzero_distribution, alpha=0.7, s=10)
                plt.plot(log_nonzero_degrees, poly(log_nonzero_degrees), color='red', label='Fitted Line')
                plt.xlabel('Degree(log)')
                plt.ylabel('Frequency(log)')
                plt.title(f'Degree Distribution of {coin_name} Degree: {lambda_value}')
                plt.savefig(save_degree_path)
                plt.close()

                centrality_data = {"Eigenvector Centrality": e_v, "Closeness Centrality": b_v, "Betweenness Centrality": c_v}
                for centrality_name, centrality_values in centrality_data.items():
                    if centrality_values:
                        save_centrality_path = f"{new_directory}/{coin_name}_{centrality_name.lower().replace(' ', '_')}.png"
                        centrality_values_counts = {}
                        for value in centrality_values:
                            centrality_values_counts[value] = centrality_values_counts.get(value, 0) + 1
                        max_frequency_value = max(centrality_values_counts, key=centrality_values_counts.get)
                        max_frequency = centrality_values_counts[max_frequency_value]
                        x = list(centrality_values_counts.keys())
                        y = list(centrality_values_counts.values())
                        x_log = [np.log10(val) for val in x]
                        y_log = [np.log10(val) for val in y]
                        plt.scatter(x_log, y_log, alpha=0.7)
                        plt.xlabel(f'{centrality_name}')
                        plt.ylabel('Frequency')
                        plt.title(f'{centrality_name} Distribution of {coin_name}')
                        plt.savefig(save_centrality_path)
                        plt.close()
                        eth_df.loc[eth_df["Name"] == coin_name, centrality_name] = f"{max_frequency},{max_frequency_value}"

                eth_df.loc[eth_df["Name"] == coin_name, "degree_lambda"] = lambda_value

    eth_df.to_csv(eth_csv_path, index=False)

# # 使用示例
# new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/nor_data_price"
# eth_csv_path = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
# process_single_folder_directory(new_directory, eth_csv_path)


def price_exist(nor_rg):
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    save_dic = f"D:/Research_PostGraduate/web3/tweet/alldata/price_api_{nor_rg}"
    eth_df = pd.read_csv(eth_dic)
    for filename in tqdm(os.listdir(save_dic), desc="Processing unique topics"):
        if filename.endswith(".json"):
            file_path = os.path.join(save_dic, filename)
            coin_name = os.path.splitext(filename)[0][:-6]

            with open(file_path, "r") as f:
                data = json.load(f)
            if data.get("data") is None or (data.get("code") == 429 and data.get("message") == "RequestLimitExceeded"):
                price_exist = 0
            else:
                price_exist = 1

            eth_df.loc[eth_df["Name"] == coin_name, "price_exist"] = price_exist
    eth_df.to_csv(eth_dic, index=False)