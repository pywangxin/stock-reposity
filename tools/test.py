import tushare as ts
import pandas as pd
import datetime


#df = ts.pro_bar(ts_code='502056.SH', asset='FD', ma=[10], start_date='20100101')

# 把trade_date设置为索引
#df.index = df['trade_date']

#print(df['20201009']['pre_close'])

# df = ts.pro_bar(ts_code='159948.SZ', asset='FD', ma=[10], start_date='20200116')



#df.iloc[0]['单价'] = 1.22

# df = df.append(pd.DataFrame([['1.33','1.33','1.33']]),ignore_index=True)
# df = df.append(pd.DataFrame([['1.44','1.55','1.66']]),ignore_index=True)
# print(df)

# file = 'data/99fundTradeData.csv'
# df.to_csv(file)
# 读取基金列表
file = '../data/01fundData.csv'
df = pd.read_csv(file)
ts_codeList = list()
# df1 = df[(df['ts_code'] == '502056.SH')]
# 对所有的基金坐下刷选
for i in df.index:
    if df.loc[i]["invest_type"] == '被动指数型' and df.loc[i]["type"] == '契约型开放式' and df.loc[i]["fund_type"] == '股票型':
        ts_codeList.append(df.loc[i]["ts_code"])

tagetYear = '2020'
file = '../data/02fundTrade+'+tagetYear+'Data.csv'
csvdf = pd.read_csv(file)
csvdf.columns=['n','ts_code', 'trade_date', 'pre_close', 'open', 'high', 'low', 'close',
       'change', 'pct_chg', 'vol', 'amount', 'ma10', 'ma_v_10']
# for j in ts_codeList:
df1 = csvdf[(csvdf['ts_code'] == '502056.SH')]

print(df1)