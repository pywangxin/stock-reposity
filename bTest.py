import tushare as ts
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import math
# 获取基金数据

df = ts.pro_bar(ts_code='512800.SH', asset='FD', ma=[10], start_date='20100101')

# 把trade_date设置为索引
df.index = df['trade_date']

# 遍历数据并且开始交易
capital_base = 100000  # 起始资金设定为100万
history_capital = list()  # 用于记录交易结果
tradeList = pd.DataFrame()

# 生成时间轴
def date_range(start, end, step=1, format="%Y%m%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


date_list = date_range("20190101", "20191231")  # 生成2016-01-01至2016-12-31的所有时间点

buyprice = 0  # 触发买入交易前
for cur_date in date_list:
    if cur_date in df.index:  # 判断当前日期是否开市交易
        # 如果T天出现收盘价格大于MA10，就在T+1的交易日的收盘价买入股票
        if df.loc[cur_date]['close'] >= df.loc[cur_date]['ma10'] and buyprice == 0:
            cur_date2 = int(cur_date) +1
            cur_date2 = str(cur_date2)
            for i in date_list:
                if cur_date2 in df.index:
                    buyprice = df.loc[cur_date2]['close']
                    num = round(capital_base / buyprice)  # 买入的基金份额
                    tradeList = tradeList.append(pd.DataFrame([[str(buyprice), str(num), cur_date2,"B",str(capital_base)]]), ignore_index=True)
                    break
                else:
                    cur_date2 = int(cur_date2) + 1
                    cur_date2 = str(cur_date2)
                    continue
        # 如果T天出现收盘价格小于MA10，就在T+1的交易日的开盘价卖出股票
        elif df.loc[cur_date]['close'] < df.loc[cur_date]['ma10'] and buyprice != 0:
            cur_date3 = int(cur_date) +1
            cur_date3 = str(cur_date3)
            for i in df.index:
                if cur_date3 in df.index:
                    sellprice = df.loc[cur_date3]['open']
                    capital_base = num * sellprice
                    buyprice = 0
                    history_capital.append(capital_base)  # 记录本次操作后剩余的资金
                    tradeList = tradeList.append(pd.DataFrame([[str(sellprice), str(num), cur_date3,"S",str(capital_base)]]), ignore_index=True)
                    break
                else:
                    cur_date3 = int(cur_date3) + 1
                    cur_date3 = str(cur_date3)
                    continue
net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0]  # 计算回测结果
# log.logger.info("total_profit：" + str(round(net_rate * 100, 2)) + "%")
tradeList.columns = ['单价',"交易数量","交易日期","交易方式","交易额"]
# print(tradeList)
file = 'data/00fundTradeData.csv'
tradeList.to_csv(file)
print(net_rate);
# plt.subplot(111)
# lable_x = np.arange(len(history_capital))
# plt.plot(lable_x, history_capital, color="r", linewidth=1.0, linestyle="-")
# plt.xlim(lable_x.min(), lable_x.max() * 1.1)
# plt.ylim(min(history_capital) * 0.9, max(history_capital) * 1.1)
# plt.grid(True)
# plt.show()
