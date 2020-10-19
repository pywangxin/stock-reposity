import pandas as pd

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
tradeData.sort_values(by="trade_date", axis=0, ascending=True, inplace=True)
# 一个一个目标基金算收益率，并记录下来
file = 'data/03fundTradeData.csv'
tradeList = pd.DataFrame()
i = 0
stockNetrate = pd.DataFrame()
# for ts_code in fundData["ts_code"]:
ts_code = '512400.SH'
if  ts_code :
    # ts_code = '513680.SZ'
    # 取出股票的日行情
    stockTradeData = tradeData[(tradeData['ts_code'] == ts_code)]
    stockTradeData.index = [i for i in range(0, len(stockTradeData.index), 1)]
    print(stockTradeData)
    # print(df.index)
    # 遍历数据并且开始交易
    capital_base = 100000  # 起始资金设定为10万
    history_capital = list()  # 用于记录交易结果
    buyprice = 0  # 触发买入交易前
    for tdate in stockTradeData.index:  # 所有交易日期遍历
        # 如果T天出现收盘价格大于MA10，就在T+1的交易日的收盘价买入股票
        if stockTradeData.loc[tdate]['close'] >= stockTradeData.loc[tdate]['ma10'] and stockTradeData.loc[tdate][
            'ma3'] > stockTradeData.loc[tdate]['ma5'] > stockTradeData.loc[tdate]['ma10'] and buyprice == 0:
            if tdate + 1 < len(stockTradeData.index):
                buyprice = stockTradeData.loc[tdate + 1]['close']
                num = round(capital_base / buyprice)  # 买入的基金份额
                history_capital.append(capital_base)
                tradeList = tradeList.append(
                    pd.DataFrame([[ts_code, str(buyprice), str(num), stockTradeData.loc[tdate]['trade_date'], "B",
                                   str(capital_base), '0']]),
                    ignore_index=True)
        # 如果T天出现收盘价格小于MA5，就在T+1的交易日的开盘价卖出股票
        elif stockTradeData.loc[tdate]['ma3'] < stockTradeData.loc[tdate]['ma5'] and buyprice != 0:
            if tdate + 1 < len(stockTradeData.index):
                sellprice = stockTradeData.loc[tdate + 1]['open']
                capital_base = num * sellprice
                buyprice = 0
                history_capital.append(capital_base)  # 记录本次操作后剩余的资金
                net_rate = (history_capital[-1] - history_capital[-2]) / history_capital[-2] * 100
                tradeList = tradeList.append(
                    pd.DataFrame(
                        [[ts_code, str(sellprice), str(num), stockTradeData.loc[tdate]['trade_date'], "S",
                          str(capital_base), net_rate]]),
                    ignore_index=True)
    if (len(history_capital) > 1):
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
