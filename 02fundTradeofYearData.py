import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time

# 读取基金列表
# file = 'data/01fundData.csv'
# fundData = pd.read_csv(file)
# # 对所有的基金坐下刷选
# fundData = fundData[(fundData["name"].str.contains('ETF')) &(fundData["invest_type"] == '被动指数型') & (fundData["type"] == '契约型开放式')&(fundData["fund_type"] == '股票型')]

# 按年获取目标基金的日交易数据并写入文件
tagetYear = '2019'
file = 'data/02fundTrade'+tagetYear+'Data.csv'
# for ts_code in fundData["ts_code"]:
ts_code = '510300.SH'
if  ts_code :
    tradeData = ts.pro_bar(ts_code=ts_code, asset='FD', ma=[5,10,15,30,60], start_date='20160701',end_date='20201010')
    tradeData.to_csv(file,mode='a',header=False)
    print(ts_code)
    time.sleep(0.5)


