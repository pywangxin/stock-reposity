import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time

df = ts.pro_bar(ts_code='502056.SH', asset='FD', ma=[10], start_date='20200915')
print(df.columns)
print(df)

