import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time
#ts.set_token("5e46738503ae00d071841f65b3472d1f51c352f453b4d63229f2a200")
df = ts.pro_bar(ts_code='502056.SH', asset='FD', ma=[10], start_date='20200101')
# print(df.columns)
# print(df)

print(df[(df["ts_code"] =="502056.SH") & (df["trade_date"] =="20201012")])

# print(df.loc[1])
