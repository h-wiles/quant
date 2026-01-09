import baostock as bs
import pandas as pd
import numpy as np

lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)


rs = bs.query_history_k_data_plus("sh.600000",
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                  start_date='2025-07-01', end_date='2025-12-31',
                                  frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:' + rs.error_code)
print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)


data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)


result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
print(result)


bs.logout()
