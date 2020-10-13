import tushare as ts
import pandas
import datetime


ts.set_token('5e46738503ae00d071841f65b3472d1f51c352f453b4d63229f2a200')
pro = ts.pro_api()
# 获取所有指数数据
df = pro.index_basic(market='CSI')
file = 'data/03indexData.csv'
df.to_csv(file)
print('is ok')
print('is ok')