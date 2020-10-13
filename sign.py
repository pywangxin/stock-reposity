import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time

# 读取基金列表
file = 'data/02fundData.csv'
df = pd.read_csv(file)
ts_codeList = list()
ts_codetagetList = list()
#遍历
#df.index = df["invest_type"]
for i in df.index:
    if df.loc[i]["invest_type"] == '被动指数型' and df.loc[i]["type"] == '契约型开放式' and df.loc[i]["status"] == 'L' and df.loc[i]["fund_type"] == '股票型':
        ts_codeList.append(df.loc[i]["ts_code"])
file = 'data/99tagetData.csv'
for j in ts_codeList:
    df = ts.pro_bar(ts_code= j, asset='FD', ma=[10], start_date='20200915')
    if df.loc[0]['close'] >= df.loc[0]['ma10']:
       ts_codetagetList.append(j)
    time.sleep(1)
    print(j)
    print(df)
df2 = pd.DataFrame(data = ts_codetagetList)
df2.to_csv(file,mode='a', header=False);
# print(df3)
print(ts_codetagetList)
# print(ts_codeList)
# print(len(ts_codeList))
