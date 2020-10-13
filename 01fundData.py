import tushare as ts
import pandas
import datetime

pro = ts.pro_api()
# 获取所有基金的数据
df = pro.fund_basic(market='E', status='L')
file = 'data/01fundData.csv'
df.to_csv(file)

