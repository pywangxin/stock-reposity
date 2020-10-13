import tushare as ts
import pandas
import datetime

pro = ts.pro_api()
# 获取所有指数数据
df = pro.fund_basic(market='E', status='L')
file = 'data/02fundData.csv'
df.to_csv(file)
print(df)
