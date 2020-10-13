# ETF基金MA10交易策略
# 1、买入：收盘指数值 >= MA10 则 买入指数对应的ETF基金
# 2、卖出：收盘指数值 < MA10 则 卖出指数对应的ETF基金
# 3、跟踪的指数池包含了以下：
# 1、确定指数池
#    1-1  宽基：
# 0   000001.SH  上证指数
# 3   000016.SH   上证50
# 4   000300.SH   沪深300
# 5   000905.SH   中证500
# 6   399001.SZ   深证成指
# 7   399005.SZ   中小板指
# 8   399006.SZ   创业板指
#  1-2 行业/主题指数：
#   0  399975.SZ  证券公司
#   1  399932.SZ  中证消费
#   2  399986.SZ 中证银行
#   3 399967.SZ 中证军工
#   4 399976.SZ CS新能车
#   5  000933.SH 中证医药
#   6 980017.SZ 国证芯片
#   7 000993.SH 全脂信息
#   8  399928.sz  中证能源
#   9  000827.sh  中证环保
import tushare as ts
import pandas as pd
import datetime

# 获取指数行情
# 参数指数代码，基金上市时间

todayTime = datetime.datetime.now()


def getStockDaily(ts_code):
    df = ts.pro_bar(ts_code=ts_code, asset='FD', ma=[10], start_date='20190101')
    return df

# 循环读取csv内的目标基金数据进行基金数据的读取
print(getStockDaily('512970.SH'))