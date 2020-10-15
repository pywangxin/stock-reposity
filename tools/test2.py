import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time

# file = '../data/01fundData.csv'
# fundData = pd.read_csv(file)
# # 对所有的基金坐下刷选
# fundData = fundData[(fundData["name"].str.contains('ETF') ) & (fundData["type"] == '契约型开放式')&(fundData["fund_type"] == '股票型')]
# print(fundData)

#
tradeData = ts.pro_bar(ts_code="159820.SZ", asset='FD', ma=[3,5,10], start_date="20191010")
print(tradeData)
print(tradeData.columns)
# stockNetrate =list()
#
# print(pd.DataFrame([[stockNetrate]]))