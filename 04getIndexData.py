import tushare as ts
import pandas as pd

#获取指数的大盘数据
pro = ts.pro_api()

df = pro.index_dailybasic(trade_date='20201009')
#df = pro.index_dailybasic(ts_code='000300.SH')
#file = 'data/04index000300.csv'
#df.to_csv(file)
#df = pro.index_weight(index_code='000300.SH', start_date='20180901', end_date='201
'''df = pro.index_weight(index_code='000300.SH')
file = 'data/04index000300weight.csv'
df.to_csv(file)
'''
print(df)
