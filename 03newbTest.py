import tushare as ts
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import math
import time

# 获取目标ts_code
# 读取基金列表
file = 'data/01fundData.csv'
fundData = pd.read_csv(file)
# 对所有的基金坐下刷选
fundData = fundData[
    (fundData["name"].str.contains('ETF')) & (fundData["type"] == '契约型开放式') & (fundData["fund_type"] == '股票型')]

# 获取基金日行情数据
tagetYear = '2019'
file = 'data/02fundTrade' + tagetYear + 'Data.csv'
tradeData = pd.read_csv(file)
tradeData.columns = ['seq', 'ts_code', 'trade_date', 'pre_close', 'open', 'high', 'low', 'close',
                     'change', 'pct_chg', 'vol', 'amount', 'ma3', 'ma_v_3', 'ma5', 'ma_v_5',
                     'ma10', 'ma_v_10']

# 一个一个目标基金算收益率，并记录下来
file = 'data/03fundTradeData.csv'
# tradeList = pd.DataFrame(columns = ['股票代码','单价',"交易数量","交易日期","交易方式","交易额",'累计收益率'])
tradeList = pd.DataFrame()


# 生成时间轴
def date_range(start, end, step=1, format="%Y%m%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


date_list = date_range(tagetYear + "0101", tagetYear + "1231")  # 生成2016-01-01至2016-12-31的所有时间点
i = 0

# def countRate(date_range,ts_code,tradDate):
stockNetrate = pd.DataFrame()
for ts_code in fundData["ts_code"]:
    # ts_code = '159820.SZ'
    # 取出股票的日行情
    stockTradeData = tradeData[(tradeData['ts_code'] == ts_code)]
    stockTradeData.index = stockTradeData['trade_date'].astype(str)
    # print(df.index)
    # 遍历数据并且开始交易
    capital_base = 100000  # 起始资金设定为100万
    history_capital = list()  # 用于记录交易结果
    buyPrice = 0  # 触发买入交易前
    for tdate in date_list:
        if tdate in stockTradeData.index:  # 判断当前日期是否开市交易
            # ma5 > ma10
            if stockTradeData.loc[tdate]['ma10'] < stockTradeData.loc[tdate]['ma5'] < stockTradeData.loc[tdate]['ma3']:
                # 如果T天出现收盘价格大于MA10，就在T+1的交易日的收盘价买入股票
                if stockTradeData.loc[tdate]['close'] >= stockTradeData.loc[tdate]['ma10'] and buyPrice == 0:
                    tdate2 = datetime.datetime.strftime(
                        datetime.datetime.strptime(tdate, "%Y%m%d") + datetime.timedelta(days=1), "%Y%m%d")
                    while 1:
                        if tdate2 in stockTradeData.index and stockTradeData.loc[tdate2]['open'] > stockTradeData.loc[tdate]['close']:
                            buyPrice = stockTradeData.loc[tdate2]['close']
                            num = round(capital_base / buyPrice)  # 买入的基金份额
                            history_capital.append(capital_base)
                            tradeList = tradeList.append(
                                pd.DataFrame(
                                    [[ts_code, str(buyPrice), str(num), tdate2, "B", str(capital_base), '0']]),
                                ignore_index=True)
                            break
                        else:
                            tdate2 = datetime.datetime.strftime(
                                datetime.datetime.strptime(tdate2, "%Y%m%d") + datetime.timedelta(days=1), "%Y%m%d")
                            if tdate2 > "20201014":
                                break
                # 如果T天出现收盘价格小于MA5，就在T+1的交易日的开盘价卖出股票
                elif stockTradeData.loc[tdate]['close'] < stockTradeData.loc[tdate]['ma5'] and buyPrice != 0:
                    tdate2 = datetime.datetime.strftime(
                        datetime.datetime.strptime(tdate, "%Y%m%d") + datetime.timedelta(days=1), "%Y%m%d")
                    while 1:
                        if tdate2 in stockTradeData.index:
                            sellprice = stockTradeData.loc[tdate2]['open']
                            capital_base = num * sellprice
                            buyPrice = 0
                            history_capital.append(capital_base)  # 记录本次操作后剩余的资金
                            net_rate = (history_capital[-1] - history_capital[-2]) / history_capital[-2] * 100
                            tradeList = tradeList.append(
                                pd.DataFrame(
                                    [[ts_code, str(sellprice), str(num), tdate2, "S", str(capital_base), net_rate]]),
                                ignore_index=True)
                            # print(tradeList)
                            # print(net_rate);
                            break
                        else:
                            tdate2 = datetime.datetime.strftime(
                                datetime.datetime.strptime(tdate2, "%Y%m%d") + datetime.timedelta(days=1), "%Y%m%d")
                            if (tdate2 > "20201010"):
                                break
    if len(history_capital) > 1:
        net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0] * 100
        stockNetrate = stockNetrate.append(
            pd.DataFrame([[ts_code, str(history_capital[-1]), str(history_capital[0]), str(net_rate)]]),
            ignore_index=True)
    i += 1
    print(ts_code + ' 第 ' + str(i) + '个')
# print(pd.DataFrame([[stockNetrate]]))
file1 = 'data/04rate.csv'
stockNetrate.to_csv(file1)
tradeList.to_csv(file)

# plt.subplot(111)
# lable_x = np.arange(len(history_capital))
# plt.plot(lable_x, history_capital, color="r", linewidth=1.0, linestyle="-")
# plt.xlim(lable_x.min(), lable_x.max() * 1.1)
# plt.ylim(min(history_capital) * 0.9, max(history_capital) * 1.1)
# plt.grid(True)
# plt.show()
