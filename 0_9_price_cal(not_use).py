import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
def to_value(hex_str: str) -> str:
    if len(hex_str) < 3:
        return "0"
    try:
        decimal_int = int(hex_str, 16)
        string_value = str(decimal_int)
        return string_value
    except ValueError:
        return "Invalid hexadecimal value"
def swap_data():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata"
    for filename in tqdm(os.listdir(new_directory), desc="Processing unique topics"):
        if filename.endswith(".csv"):
            file_path = os.path.join(new_directory, filename)
            coin_name = os.path.splitext(filename)[0]
            df = pd.read_csv(file_path)
            coin_name_price_data = [] #{'Time': swapTime, 'From': from_add, 'To': to_add, 'Eth_price': eth_amount, 'ERC20_price': coin_amount}
            df['event_txt_clean'] = df['event_txt'].str.split('(').str[0]
            swap_rows = df[(df['event_txt_clean'] == 'Swap') & (df['data'].str.len() == 258)]
            from_list = swap_rows['topic1']
            to_list = swap_rows['topic2']
            time_list = swap_rows['date']
            from_list = swap_rows['topic1'].reset_index(drop=True)
            to_list = swap_rows['topic2'].reset_index(drop=True)
            time_list = swap_rows['date'].reset_index(drop=True)

            swap_rows_data = swap_rows['data']

            swap_rows_data_strings = [str(s)[2:] for s in swap_rows_data]
            swap_result = []
            for s in swap_rows_data_strings: #'0x,000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,000015181ff25a98,00000000000000000000000000000000000000000000000c508286014761e64dfd10000000000000000000000000000000000000000000000000000000000000000'
                for i in range(0, len(s), 64):
                    swap_result.append(s[i:i+64])

            data_hex_groups = []
            for i in range(0, len(swap_result), 4):
                data_hex_groups.append(swap_result[i:i+4])

            for i, group in enumerate(data_hex_groups):
                eth_coin_pair = []
                for item in group:
                    dec_value = to_value(item)
                    if dec_value!=str(0):
                        eth_coin_pair.append(dec_value)
                eth_coin_pair[0] = float(eth_coin_pair[0]) / 10**18
                eth_coin_pair[1] = float(eth_coin_pair[1]) / 10**9
                coin_name_price_data.append({'Time': time_list[i], 'From': from_list[i], 'To': to_list[i], 'Eth_price': eth_coin_pair[0], 'ERC20_price': eth_coin_pair[1]})
            file_path=f"D:/Research_PostGraduate/web3/tweet/alldata/price/{coin_name}_price.csv"
            coin_name_price_data_df = pd.DataFrame(coin_name_price_data)
            coin_name_price_data_df.to_csv(file_path, index=False)


# swap_data()
def price_plot():
    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/price"
    for filename in tqdm(os.listdir(new_directory), desc="Processing unique topics"):
        if filename.endswith(".csv"):
            file_path = os.path.join(new_directory, filename)
            coin_name = os.path.splitext(filename)[0]
            df = pd.read_csv(file_path)
            df['Price'] = df['Eth_price'] / df['ERC20_price']
            df['Time'] = pd.to_datetime(df['Time'])
            plt.figure(figsize=(10, 6))
            plt.scatter(df['Time'], df['Price'], s=10, c='b', marker='o', alpha=0.5)
            plt.title('Price Over Time')
            plt.xlabel('Time')
            plt.ylabel('Price')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # 保存为PNG
            plt.savefig(f'D:/Research_PostGraduate/web3/tweet/output_plot/{coin_name}_plot.png')

           

# price_plot()


def request_price():
    import requests

    symbol = "BTC"
    convert = "USD"
    url = f"https://c5d975c6-ca3c-4adb-a5f4-b081b085a080.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}&convert={convert}"

    response = requests.get(url)
    data = response.json()
    price = data["data"][symbol]["quote"][convert]["price"]

    print(f"The price of {symbol} in {convert} is {price}")
request_price()