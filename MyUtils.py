import baostock as bs
import pandas as pd

def get_stock_info(save_path="./stock_info.csv"):
    """获取所有股票代码数据"""
    try:
        # 登录系统
        bs.login()

        # 获取证券基本资料
        rs = bs.query_stock_basic()

        # 获取具体数据
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())

        # 转换为DataFrame
        result = pd.DataFrame(data_list, columns=rs.fields)
        result = result[result['type'] == "1"]
        result = result[result["code_name"].apply(lambda x: "ST" not in x)]
        result = result[result["outDate"].apply(lambda x: x == "")]

        result = result[["code", "code_name", "ipoDate", "type", "status"]]

        result.to_csv(save_path, index=False, encoding="utf-8-sig")

        print(f"获取到股票数量: {len(result)}")
        print("\n股票列表:")
        print(result.head(10))

        # 登出系统
        bs.logout()

        return result
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return None

if __name__ == '__main__':
    get_stock_info()