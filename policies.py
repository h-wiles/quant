"""
前一天日线KDJ的J到大负值，并且当天尾盘K线出现反转K形态
"""

import tushare as ts
import pandas as pd
import logging
from datetime import datetime, timedelta
from MyUtils import get_intraday_minute_data, calculate_kdj

# 创建一个Logger对象
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建一个文件处理器
file_handler = logging.FileHandler('policy_1_log.log')

# 创建一个日志格式化器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到Logger中
logger.addHandler(file_handler)

# 设置你的token
ts.set_token('xxx')
pro = ts.pro_api()

# 查询当前所有正常上市交易的股票列表
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data = data[~data['name'].str.contains('ST')]   # 除去ST股

today = datetime.today().strftime('%Y%m%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

for code in data.ts_code:
    df = pro.daily(ts_code=code)   # 获取当前股票历史K线数据
    df = df.sort_values(by=['trade_date'], ascending=True)

    kdj_df = calculate_kdj(df=df)
    kdj_today = kdj_df['j'].values[-1]
    kdj_yesterday = kdj_df['j'].values[-2]

    rt_df = pro.rt_k(ts_code=code, freq="1MIN")     # 当前股票分时数据

    amp = (rt_df['close']-rt_df['open'])/rt_df['open']

    if (kdj_today<0 or kdj_yesterday<0) and amp < 0.3/100 :
        # 输出日志信息
        logger.info('KDJ+反转K策略筛选股票: ')

