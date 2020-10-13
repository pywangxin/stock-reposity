import tushare as ts
import pandas as pd
import datetime


#df = ts.pro_bar(ts_code='502056.SH', asset='FD', ma=[10], start_date='20100101')

# 把trade_date设置为索引
#df.index = df['trade_date']

#print(df['20201009']['pre_close'])

df = ts.pro_bar(ts_code='159948.SZ', asset='FD', ma=[10], start_date='20200116')
11



#df.iloc[0]['单价'] = 1.22

# df = df.append(pd.DataFrame([['1.33','1.33','1.33']]),ignore_index=True)
# df = df.append(pd.DataFrame([['1.44','1.55','1.66']]),ignore_index=True)
print(df)

file = 'data/99fundTradeData.csv'
df.to_csv(file)