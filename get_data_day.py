import schedule
import time
import baostock as bs
import akshare as ak
import pandas as pd


def get_stocks_baostock():
    """
    使用Baostock获取A股股票列表
    """
    try:
        # 登录系统
        lg = bs.login()

        # 获取证券基本资料
        rs = bs.query_stock_basic()

        # 获取具体数据
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())

        # 转换为DataFrame
        result = pd.DataFrame(data_list, columns=rs.fields)

        print(f"获取到股票数量: {len(result)}")
        print("\n股票列表:")
        print(result.head(10))

        # 登出系统
        bs.logout()

        return result
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return None


# 定义你希望每天7点执行的任务
def get_stock_data():
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

# 每天下午7点执行任务
# schedule.every().day.at("19:00").do(task)

# 持续检查并执行定时任务
# while True:
#     schedule.run_pending()
#     time.sleep(1)  # 每秒检查一次


if __name__ == '__main__':
    result = get_stocks_baostock()