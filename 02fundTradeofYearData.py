import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time

# 读取基金列表
file = 'data/01fundData.csv'
df = pd.read_csv(file)
ts_codeList = list()
ts_codetagetList = list()

# 对所有的基金坐下刷选
for i in df.index:
    if df.loc[i]["invest_type"] == '被动指数型' and df.loc[i]["type"] == '契约型开放式' and df.loc[i]["fund_type"] == '股票型':
        ts_codeList.append(df.loc[i]["ts_code"])
# 按年获取目标基金的日交易数据并写入文件
tagetYear = '2020'
file = 'data/02fundTrade'+tagetYear+'Data.csv'
for j in ts_codeList:
    df = ts.pro_bar(ts_code=j, asset='FD', ma=[10], start_date=tagetYear+'0101',end_date=tagetYear+'1231')
    df.to_csv(file,mode='a',header=False)
    print(j)
    time.sleep(1)


