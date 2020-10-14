import tushare as ts
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import math
import time

# 获取目标ts_code
file = 'data/01fundData.csv'
df = pd.read_csv(file)
ts_codeList = list()
# 对所有的基金做下刷选
for i in df.index:
    if df.loc[i]["invest_type"] == '被动指数型' and df.loc[i]["type"] == '契约型开放式' and df.loc[i]["fund_type"] == '股票型':
        ts_codeList.append(df.loc[i]["ts_code"])
print(len(ts_codeList))
# 获取基金数据
tagetYear = '2020'
file = 'data/02fundTrade'+tagetYear+'Data.csv'
csvdf = pd.read_csv(file)
csvdf.columns=['n','ts_code', 'trade_date', 'pre_close', 'open', 'high', 'low', 'close',
       'change', 'pct_chg', 'vol', 'amount', 'ma10', 'ma_v_10']
# 一个一个目标基金算收益率，并记录下来
file = 'data/03fundTradeData.csv'
#tradeList = pd.DataFrame(columns = ['股票代码','单价',"交易数量","交易日期","交易方式","交易额",'累计收益率'])
tradeList = pd.DataFrame()
#生成时间轴
def date_range(start, end, step=1, format="%Y%m%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]
date_list = date_range(tagetYear+"0101", tagetYear+"1231")  # 生成2016-01-01至2016-12-31的所有时间点
i = 0

# def countRate(date_range,ts_code,tradDate):
# try:
for ts_code in ts_codeList:
    # 取出股票的日行情
    df = csvdf[(csvdf['ts_code'] == ts_code)]
    # 把trade_date设置为索引
    df.index = df['trade_date']
    # print(df.index)
    # 遍历数据并且开始交易
    capital_base = 100000  # 起始资金设定为100万
    history_capital = list()  # 用于记录交易结果
    buyprice = 0  # 触发买入交易前
    for tdate in date_list:
        tdate = int(tdate)
        if tdate in df.index:  # 判断当前日期是否开市交易
            # 如果T天出现收盘价格大于MA10的100%，就在T+1的交易日的收盘价买入股票
            if df.loc[tdate]['close'] >= df.loc[tdate]['ma10'] and buyprice == 0:
                td2 = datetime.datetime.strptime(str(tdate), format("%Y%m%d")) + datetime.timedelta(days=1)  # 获取下一天的价格
                td2 = datetime.datetime.strftime(td2, format("%Y%m%d"))
                td2 = int(td2)
                while 1:
                    if (td2 in df.index):
                        buyprice = df.loc[td2]['close']
                        num = round(capital_base / buyprice)  # 买入的基金份额
                        tradeList = tradeList.append(
                            pd.DataFrame([[ts_code, str(buyprice), str(num), td2, "B", str(capital_base), '0']]),
                            ignore_index=True)
                        break
                    else:
                        td2 = datetime.datetime.strptime(str(td2), format("%Y%m%d")) + datetime.timedelta(
                            days=1)  # 获取下一天的价格
                        td2 = datetime.datetime.strftime(td2, format("%Y%m%d"))
                        td2 = int(td2)
                        # if (td2 > 20201010):
                        #     break
            # 如果T天出现最低价价格小于MA10的，就在T+1的交易日的开盘价卖出股票
            elif df.loc[tdate]['low'] < df.loc[tdate]['ma10'] and buyprice != 0:
                td2 = datetime.datetime.strptime(str(tdate), format("%Y%m%d")) + datetime.timedelta(
                    days=1)  # 获取下一天
                td2 = datetime.datetime.strftime(td2, format("%Y%m%d"))
                td2 = int(td2)
                while 1:
                    if td2 in df.index:
                        sellprice = df.loc[td2]['open']
                        capital_base = num * sellprice
                        buyprice = 0
                        history_capital.append(capital_base)  # 记录本次操作后剩余的资金
                        net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0] * 100
                        tradeList = tradeList.append(
                            pd.DataFrame(
                                [[ts_code, str(sellprice), str(num), td2, "S", str(capital_base), net_rate]]),
                            ignore_index=True)
                        # print(tradeList)
                        # print(net_rate);
                        break
                    else:
                        td2 = datetime.datetime.strptime(str(td2), format("%Y%m%d")) + datetime.timedelta(
                            days=1)  # 获取下一天
                        td2 = datetime.datetime.strftime(td2, format("%Y%m%d"))
                        td2 = int(td2)
                        # if(td2 > 20201010):
                        #     break

i += 1
    # if (i > 100):
    #     break
print(ts_code + 'di  ' + str(i))
# except Exception as e:
#     if e.__class__ == KeyboardInterrupt:  # if keyboard interruption is caught
#         raise KeyboardInterrupt
print("nice")
tradeList.to_csv(file)


# plt.subplot(111)
# lable_x = np.arange(len(history_capital))
# plt.plot(lable_x, history_capital, color="r", linewidth=1.0, linestyle="-")
# plt.xlim(lable_x.min(), lable_x.max() * 1.1)
# plt.ylim(min(history_capital) * 0.9, max(history_capital) * 1.1)
# plt.grid(True)
# plt.show()
