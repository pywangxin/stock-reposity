import tushare as ts
import pandas as pd
import datetime

#pro = ts.pro_api('5e46738503ae00d071841f65b3472d1f51c352f453b4d63229f2a200')
# 获取所有股票信息
'''
df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
file = 'data/01stockdata.csv'
df.to_csv(file)
print(df)
'''
# 获取股票每日指标数据
pro = ts.pro_api()
df = pro.daily_basic(ts_code='000001.sz')
file = 'data/000001Dailydata.csv'
df.to_csv(file)
print(df)

