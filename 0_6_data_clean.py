import pandas as pd
import matplotlib.pyplot as plt
import os
events_df = pd.read_csv("events.csv")

directory = "D:/Research_PostGraduate/web3/tweet/alldata/0_nor_pool_confirm"

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        
        file_path = os.path.join(directory, filename)
        print(f"name: {file_path}")
        df = pd.read_csv(file_path)
        rows_before = df.shape[0]
        print(f"处理前 {filename} 的行数: {rows_before}")
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df = df.drop_duplicates()

        new_file_path = os.path.join(directory, f"{filename}")
        df.to_csv(new_file_path, index=False)

        rows_after = df.shape[0]
        print(f"处理后 {filename} 的行数: {rows_after}")
        print(f"共删除了 {rows_before - rows_after} 个重复行")
        print("---")


# event_signatures = wanted_df["topic0"]

# event_signature_counts = event_signatures.value_counts()

# event_signature_to_name = events_df.set_index('Event Signature')['Event Name'].to_dict()
# event_signature_counts.index = event_signature_counts.index.map(event_signature_to_name)

# plt.figure(figsize=(15, 8))
# event_signature_counts.plot(kind='pie', autopct='%1.1f%%', labeldistance=1.1, startangle=140, pctdistance=0.85, counterclock=False , cmap='tab20c', wedgeprops=dict(width=0.4))
# plt.axis('equal')

# plt.legend(loc="center right")  # 将图例放置在图表外部
# plt.title('Event Signature Frequency of Token wanted')
# plt.show()