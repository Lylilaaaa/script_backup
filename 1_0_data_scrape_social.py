from Scweet.scweet import scrape
import pandas as pd
from tqdm import tqdm
import os
from datetime import datetime, timedelta
import time
from Scweet.scweet import scrape_certain_link

# ========================= scrape twitter content =========================
def get_data_from_twi():
    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum_final.csv"
    # Name,Market,Chain,Address,Social,ID,WarningText,Rugpull_level,WarningText_trans,address_code,Rugpull_comfirm,price_exist
    eth_df = pd.read_csv(eth_dic, encoding='ISO-8859-1')
    # print(eth_df.columns)

    new_directory = "D:/Research_PostGraduate/web3/tweet/alldata/0_rugpull_pool_confirm"
    for file in tqdm(os.listdir(new_directory), desc="Processing unique topics"):
        if file.endswith(".csv"):
            coin_name = os.path.splitext(file)[0]
            coin_name = coin_name[:-5]
            print("name: ",coin_name)
            # if coin_name.endswith("_clean"):
            path = os.path.join(new_directory, file)
            coin_df = pd.read_csv(path)
            # coin_name = coin_name[:-6]
            coin_name_value = eth_df.loc[eth_df['Name'] == coin_name, 'Coin_name'].values[0]
            start_date = coin_df['date'].iloc[0]  # 修正了索引方式
            start_date_without_tz = start_date[:-4]  # 去除 ' UTC'
            start_date_date = datetime.strptime(start_date_without_tz, "%Y-%m-%d %H:%M:%S").date()
            end_date = start_date_date + timedelta(days=30)
            print(coin_name_value, start_date_date,end_date)
            #'MONG', 'AKITA', 'BABYSHIBA', 'BAG', 'BARA', 'BIAO', 'BOG', 'BREPE', 'BTCPEP', 'BULL', 'BUTTER', 'CHAD', 'CHECKS', 'COPE', 'COSHI', 'CRYPTO', 'CUT', 'DC', 'DERP', 'DINGER', 'DOE', 'DOGIRA', 'DOGTIC', 'DUCKER', 'DUMMY', 'ELMO', 'ETHEREUM', 'EVILPEPE', 'FANTA', 'FINALE', 'FLEX', 'FOFO', 'FONZY', 'FROGEX', 'FROKI', 'GENSLR', 'GENW', 'GMEME', 'GOOCH', 'GUSTA', 'GYOSHI', 'HER', 'HOKK', 'HONK', 'JEFF', 'JESUS', 'JIM', 'KAWA', 'KEKE', 'KEKO', 'LADYS', 'LARRY', 'MEM', 'MONKED', 'MONKE', 'MPEPE', 'NARUTO', 'NEZUKO', 'OGMF', 'PEPES', 'PEPEXL', 'POOPE', 'POPE', 'PPBLZ', 'PP', 'PSYOP',
            #                           'PUSSY', 'QOM', 'RON', 'RYOSHI', 'SHIBELON', 'SHIBGF', 'SHINU', 'SHIRD', 'SHS', 'SMUDGE', 'SPX', 'TATE', 'TIPJA', 'TRUTH', 'VERSE', 'VINU', 'WAGMI', 'YEET'
            # if coin_name_value not in['$420CHAN', '$BABYBITCOIN', '$BASED', '$BERT', '$BOOBY', '$CHOO', '$NUDE', '$PINCHI', '0XT', '2.0PEPE', '404A', '4CHAN', '6PR', '8BIT', '9998', 'AANG', 'AGB', 'AII', 'AI', 'AKAMARU', 'AKITA', 'AKITA', 'AKITA', 'ANDY', 'APED', 'APEPE', 'APU', 'APU', 'APX', 'ARTHUR', 'ASH', 'ASPC', 'ASUKA', 'AUT', 'AWOKE', 'AXL', 'BABYDOGE2.0', 'BABYDOGE2.0', 'BABYGROK', 'BABYJESUS', 'BABYMAGA', 'BABYMEME', 'BABYSHIBA', 'BABYSHIBA', 'BABYSHIBA', 'BABYTRUMP', 'BABYTRUMP', 'BAD', 'BAG', 'BAG', 'BAG', 'BALD2', 'BALD', 'BARA', 'BARA', 'BARA', 'BASED', 'BBPP', 'BBRICK', 'BEAST', 'BEBE', 'BEB', 'BEE', 'BENDER', 'BGTT', 'BIAO', 'BIAO', 'BIAO', 'BIBLE', 'BIDEN', 'BIRD', 'BITCONNECT2.0', 'BIZ', 'BLADESOFGLORY', 'BOBO', 'BOB', 'BOG', 'BOG', 'BOG', 'BOG', 'BOI', 'BONE2.0', 'BOOM', 'BORING', 'BPD', 'BPEPE2.0', 'BPEPE', 'BREPE', 'BREPE', 'BREPE', 'BRO', 'BTB', 'BTCPEP', 'BTCPEP', 'BTCPEP', 'BTFD', 'BUBS', 'BUBU', 'BUGATTI', 'BULLMOON', 'BULLS', 'BULL', 'BULL', 'BULL', 'BURNBB', 'BUTTER', 'BUTTER', 'BUTTER', 'BUZZ', 'BWSM', 'BYTE', 'CAL', 'CAO CAO', 'CAPT', 'CAPY', 'CAT.AI', 'CATCH', 'CATE', 'CATS', 'CF', 'CHAD', 'CHAD', 'CHAD', 'CHAMPZ', 'CHECKDM', 'CHECKS', 'CHECKS', 'CHECKS', 'CHIBI', 'CHMPZ', 'CHOPPY', 'CHOW', 'CHUPE', 'CLAVELL', 'CLUB', 'COOM', 'COPE', 'COPE', 'COPE', 'COSHI', 'COSHI', 'COSHI', 'COVID', 'CRAZYPEPE', 'CRAZY', 'CRIMINGO', 'CRYPTO', 'CRYPTO', 'CRYPTO', 'CR', 'CSI', 'CUJO', 'CUT', 'CUT', 'CUT', 'CV', 'CX', 'CYBONK', 'DABABY', 'DACAT', 'DAD', 'DAO', 'DAVID', 'DAWG', 'DC', 'DC', 'DC', 'DEFROGS', 'DERP', 'DERP', 'DERP', 'DFV', 'DIBBLE', 'DICK', 'DINGER', 'DINGER', 'DINGER', 'DISCORD', 'DOE', 'DOE', 'DOE', 'DOGDEFI', 'DOGIRA', 'DOGIRA', 'DOGIRA', 'DOGTIC', 'DOGTIC', 'DOGTIC', 'DOOM', 'DRF', 'DROPS', 'DUCKER', 'DUCKER', 'DUCKER', 'DUMMY', 'DUMMY', 'DUMMY', 'DYOR', 'EGG', 'ELMO', 'ELMO', 'ELMO', 'ELONIUM', 'FANTA', 'FANTA', 'FANTA', 'FEFE', 'FINALE', 'FINALE', 'FINALE', 'FINU', 'FLEX', 'FLEX', 'FLEX', 'FOFO', 'FOFO', 'FOFO', 'FONZY', 'FONZY', 'FONZY', 'FROGEX', 'FROGEX', 'FROGEX', 'FROKI', 'FROKI', 'FROKI', 'GENSLR', 'GENSLR', 'GENSLR', 'GENW', 'GENW', 'GENW', 'GMEME', 'GMEME', 'GMEME', 'GOOCH', 'GOOCH', 'GOOCH', 'GUSTA', 'GUSTA', 'GUSTA', 'GYOSHI', 'GYOSHI', 'GYOSHI', 'HER', 'HER', 'HER', 'HOKK', 'HOKK', 'HOKK', 'HONK', 'HONK', 'HONK', 'JEFF', 'JEFF', 'JEFF', 'JESUS', 'JESUS', 'JESUS', 'JIM', 'JIM', 'JIM', 'JIM', 'KAWA', 'KAWA', 'KAWA', 'KEKE', 'KEKE', 'KEKE', 'KEKO', 'KEKO', 'KEKO', 'KENNY', 'LADYS', 'LADYS', 'LADYS', 'LARRY', 'LARRY', 'LARRY', 'MEM', 'MEM', 'MEM', 'MILKIT', 'MONG', 'MONG', 'MONG', 'MONKED', 'MONKED', 'MONKED', 'MONKE', 'MONKE', 'MONKE', 'MPEPE', 'MPEPE', 'MPEPE', 'NANA', 'NARUTO', 'NARUTO', 'NARUTO', 'NARUTO', 'NEZUKO', 'NEZUKO', 'NEZUKO', 'NEZUKO', 'OGMF', 'OGMF', 'OGMF', 'OMIKAMI', 'PEPES', 'PEPES', 'PEPES', 'PEPES', 'PEPEXL', 'PEPEXL', 'PEPEXL', 'PEPITO', 'POOPE', 'POOPE', 'POOPE', 'POPE', 'POPE', 'POPE', 'POPE', 'PPBLZ', 'PPBLZ', 'PPBLZ', 'PP', 'PP', 'PP', 'PSPS', 'PSYOP', 'PSYOP', 'PUSSY', 'QOM', 'REGULATEIT', 'RON', 'RYOSHI', 'SHIBELON', 'SHIBGF', 'SHIBIT', 'SHINU', 'SHIRD', 'SHS', 'SMUDGE', 'SPX', 'TATE', 'TIPJA', 'TOTOFO', 'TRUTH', 'VERSE', 'VINU', 'WAGMI', 'X', 'YEET', 'YOBASE', 'ZINU']: # ,'$HER',COSHI,,'CUT','DERP','DINGER'
            if coin_name_value not in['$BABYBITCOIN', '$REKT', '2.0PEPE', 'ASPC', 'ASUKA', 'AWOKE', 'BASED', 'BEAST', 'BEE', 'BITCOIN2.0', 'BLADESOFGLORY', 'BTCPEP', 'BUBS', 'CAPT', 'CAT.AI', 'CROOGE', 'CUJO', 'DANK', 'DOGIRA', 'DOOM', 'DRF', 'DROPS', 'DYOR', 'EGG', 'ELONIUM', 'FANTA', 'FEFE', 'FINU', 'FLOKI 2.0', 'FOMC', 'FORCE', 'FOSSA', 'FROKI', 'GARFIELD', 'GFSHIB', 'GHOST', 'GRETA', 'HEHE', 'HEROES', 'HIPPO', 'HOMER', 'HOPPY2.0', 'HPNY2024', 'KENNY', 'MDMA', 'MEOW', 'MEWTWO', 'MONKED', 'MRX', 'MXRC', 'NPC', 'ONG', 'PANDEE', 'PEPE XAI', 'PEPEAI', 'PEPECOLA', 'PEPITO', 'PEPUMP', 'PHUB', 'PMC', 'POM', 'POTTERINU', 'PREZ', 'RIPDIP', 'SAFEREUM', 'SCRAPPY', 'SENDIT', 'SSB']:
                data = scrape(words=[f"${coin_name_value}"], since = str(start_date_date), until = str(end_date), from_account=None,
                            interval=1,
                            headless=False, display_type="Latest", save_images=False, proxy="http://127.0.0.1:7890", save_dir='outputs/social_data_rug_pull',
                            resume=False, filter_replies=True, proximity=False,env=".env")
                time.sleep(500)
get_data_from_twi()

def print_got_list():
    name_list = []
    for files in tqdm(os.listdir("D:/Research_PostGraduate/web3/tweet/outputs/social_data_rug_pull"), desc="Processing unique topics"):
        if files.endswith(".csv"):
            coin_name = os.path.splitext(files)[0]
            coin_name = coin_name.split("_")
            coin_name = coin_name[0]
            coin_name = coin_name[1:]
            name_list.append(coin_name)
    print(name_list)
# print_got_list()


# ========================= scrape retweet from links =========================
def convert_to_int(value):
    if isinstance(value, str) and 'K' in value:
        return int(float(value.replace('K', '')) * 1000)
    elif isinstance(value, (int, float)):
        return int(value)
    else:
        return 0

def get_reweet():
    path = "D:/Research_PostGraduate/web3/tweet/outputs/social_data"
    for files in tqdm(os.listdir(path), desc="Processing unique topics"):
        if files.endswith(".csv"):
            coin_name_ = os.path.splitext(files)[0]
            coin_name = coin_name_.split("_")
            coin_name = coin_name[0]
            coin_name = coin_name[1:]
            # if coin_name not in['AKITA', 'BABYSHIBA', 'BAG', 'BARA', 'BIAO', 'BOG', 'BREPE', 'BTCPEP', 'BULL', 'BUTTER', 'CHAD', 'CHECKS', 'COPE', 'COSHI', 'CRYPTO', 'CUT', 'DC', 'DERP', 'DINGER', 'DOE', 'DOGIRA', 'DOGTIC', 'DUCKER', 'DUMMY', 'ELMO', 'FANTA', 'FINALE', 'FLEX', 'FOFO', 'FONZY', 'FROGEX', 'FROKI', 'GENSLR', 'GENW', 'GMEME', 'GOOCH', 'GUSTA', 'GYOSHI', 'HER', 'HOKK', 'HONK', 'JEFF', 'JESUS', 'JIM', 'KAWA', 'KEKE', 'KEKO', 'LADYS', 'LARRY', 'MEM', 'MONG', 'MONKED', 'MONKE', 'MPEPE', 'NARUTO', 'NEZUKO', 'OGMF', 'PEPES', 'PEPEXL', 'POOPE', 'POPE']:
            if coin_name not in[]:
                print(coin_name)
                ori_path = os.path.join(path, files)
                filter_path = os.path.join(path, f"{coin_name_}_filter.csv")
                data = pd.read_csv(ori_path)
                data['Retweets'] = data['Retweets'].fillna(0).apply(convert_to_int)
                filtered_data = data[data['Retweets'] >= 2]
                filtered_data.to_csv(filter_path, index=False)
                link_list = filtered_data['Tweet URL']
                data = scrape_certain_link(coin_name = f"${coin_name}",link_list = link_list,headless=False,proxy="http://127.0.0.1:7890", save_dir='outputs/social_data',env=".env")
                print(f"-----------------------FINISHI COIN: {coin_name}---------------------------------")
          
                # time.sleep(900)
# get_reweet() 

retweet_name_list = []
def print_got_list():
    for files in tqdm(os.listdir("D:/Research_PostGraduate/web3/tweet/outputs/social_data"), desc="Processing unique topics"):
        if files.endswith(".csv"):
            coin_name_ = os.path.splitext(files)[0]
            if coin_name_.endswith("_retweets_ID"):
                coin_name = str(coin_name_).split("_")
                coin_name = coin_name[0]
                coin_name = coin_name[1:]
                retweet_name_list.append(coin_name)

# print_got_list()
# print(retweet_name_list)

retweet_content_list = []
# ========================= merge retweet and content =========================
def merge_retweet_content():
    path = "D:/Research_PostGraduate/web3/tweet/outputs/social_data"
    for files in tqdm(os.listdir("D:/Research_PostGraduate/web3/tweet/outputs/social_data"), desc="Processing unique topics"):
        if files.endswith(".csv"):
            coin_name_ = os.path.splitext(files)[0]
            coin_name = coin_name_.split("_")
            coin_name = coin_name[0]
            coin_name = coin_name[1:]
            if coin_name in retweet_name_list:
                if not coin_name_.endswith("_retweets_ID"):
                    retweet_content_list.append(files)
    for i in range(0, len(retweet_content_list), 2):
        pair = retweet_content_list[i:i+2]
        path1 = os.path.join(path, pair[0])
        path2 = os.path.join(path, pair[1])
        coin_name = os.path.splitext(pair[0])[0].split("_")[0][1:]
        special_string = "$"
        save_path = os.path.join("D:/Research_PostGraduate/web3/tweet/outputs/social_data_merge", f"{special_string}{coin_name}_merged.csv")
        print(save_path)
        df1 = pd.read_csv(path1)
        df2 = pd.read_csv(path2)  
        df1.drop('Retweets IDs', axis=1, inplace=True)
        result = pd.merge(df1, df2, on='Tweet URL', how='outer')

        for index, row in result.iterrows():
            retweets_string = row['Retweets IDs']
            if isinstance(retweets_string,str):
                retweets_list = retweets_string.split(',')
                unique_retweets_set = set(retweets_list)
                unique_retweets_string = ','.join(unique_retweets_set)
                result.loc[index, 'Retweets IDs'] = unique_retweets_string
                result.loc[index, 'Unique Retweets Count'] = len(unique_retweets_set)
        result.to_csv(save_path, index=False)
# merge_retweet_content()

def get_merge():
    path = "D:/Research_PostGraduate/web3/tweet/outputs/social_data"
    df = pd.read_csv('outputs\Pepe_merged_file.csv')
    new_df = pd.DataFrame(columns=['src', 'dst','time'])
    dfs = []
    for index, row in df.iterrows():
        time = row['Timestamp']
        retweets_string = row['Retweets IDs']
        if isinstance(retweets_string, str):
            retweets_list = retweets_string.split(',')
            user_name = row['UserName']
            data = [{'src': user_name, 'dst': dst,'time': time} for dst in retweets_list]
            dfs.append(pd.DataFrame(data))
    new_df = pd.concat(dfs, ignore_index=True)
    new_df.to_csv('outputs\Pepe_edge.csv', index=False)

def price_rug_combine():
    label_list_path = "D:/Research_PostGraduate/web3/tweet/alldata/labeled_list.csv"
    # token_address,pool_address,label,type
    label_list_df = pd.read_csv(label_list_path)
    label_list_df.columns = label_list_df.columns.str.lower()  # 将列名转换为小写

    eth_dic = "D:/Research_PostGraduate/web3/tweet/outputs/coinmarketcap_detail_Ethereum.csv"
    # Name,Market,Chain,Address,Social,ID,WarningText,Rugpull_level,WarningText_trans,address_code,Rugpull_comfirm,price_exist
    eth_df = pd.read_csv(eth_dic)
    eth_df.columns = eth_df.columns.str.lower()  # 将列名转换为小写

    # 筛选label为0的token_address
    filtered_labels = label_list_df[label_list_df['label'] == 0]['token_address'].str.lower()
    print(filtered_labels)

    # 将两个 DataFrame 根据 address_code 进行合并
    merged_df = pd.merge(eth_df, filtered_labels, left_on='address_code', right_on='token_address', how='inner')
    print(eth_df['address_code'])

    # 输出匹配的内容
    print(merged_df[['token_address', 'address']])
