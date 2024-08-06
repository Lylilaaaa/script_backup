import json
from time import time
import requests
import pandas as pd

class Translate_Series:
    """
        思路：因为翻译接口有访问次数的限制，所以首先将Series重后，再调用有道翻译的接口将Series中每个数据，
        翻译成中文保存为json文件{原始数据:翻译后的数据}，然后对原始的Series进行遍历替换
    """
    def __init__(self, filename, Series):
        """
        :param filename: 路径/文件名
        :param Series: pd.Series
        """
        self.filename = filename
        self.Series = Series

    @property
    def read_json(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            return ''
        return data

    def save_json(self, data):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))

    def translation(self, string):
        """
        :param string: 需要翻译的字符串
        :return: 翻译后的字符串
        """
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': string
        }
        # proxy = {'http': '27.38.99.186:9797'}
        url = "http://fanyi.youdao.com/translate"
        try:
            res = requests.get(url, params=data)
            result = res.json()
            print(string+': '+result['translateResult'][0][0]['tgt'])
            return result['translateResult'][0][0]['tgt']
        except:
            pass

    @property
    def translation_detail(self):
        """
        :return: 字典：原始数据:翻译后的数据
        """
        begin_time = time()  # 用来获取当前的时间，返回的单位是秒
        info_unique = self.Series.unique()
        info_translation = pd.Series(info_unique)
        info_translation = info_translation.apply(lambda x: self.translation(x))
        info = {i: j for i, j in zip(info_unique, info_translation)}
        end_time = time()
        run_time = end_time - begin_time
        print(f'翻译{len(info)}条数据总耗时：{run_time}s')
        return info

    def __call__(self):
        if not self.read_json:
            self.save_json(self.translation_detail)        # 翻译保存到json文件中
        begin_time = time()
        print('正在对当前Series遍历替换...')
        res = self.Series.apply(lambda x: self.read_json[x] if not pd.isnull(x) else x)    # 对原始的Series进行遍历替换
        end_time = time()
        run_time = end_time - begin_time
        print(f'遍历替换{len(self.Series)}条数据总耗时：{run_time}s')
        return res

