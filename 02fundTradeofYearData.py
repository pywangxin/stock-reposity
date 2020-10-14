import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time

# 读取基金列表
file = 'data/01fundData.csv'
df = pd.read_csv(file)
# 对所有的基金坐下刷选
df = df[(df["invest_type"] == '被动指数型') & (df["type"] == '契约型开放式') & (df["fund_type"] == '股票型') ]
# 按年获取目标基金的日交易数据并写入文件
targetYear = '2020'
file = 'data/02fundTrade'+targetYear+'Data.csv'
for ts_code in df['ts_code']:
    fundTradeData = ts.pro_bar(ts_code=ts_code, asset='FD', ma=[10], start_date=targetYear+'0101',end_date=targetYear+'1231')
    fundTradeData.to_csv(file, mode='a',header=False)
    print(ts_code)
    time.sleep(0.5)


