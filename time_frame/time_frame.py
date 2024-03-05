import pandas as pd


def drop_duplicate(cluster, time_window=300):
    """
    以时间窗口, 处理时间数据
    :param cluster: dataframe集合
    :param time_window: 时间窗, 单位秒
    :return:
    """
    # 校验 cluster 是否正常
    if not isinstance(cluster, pd.DataFrame) or cluster.empty:
        return None

    # 校验 apper_time 是否存在
    if "apper_time" not in cluster.columns:
        return None

    # 校验 apper_time 列 是否为 pd.Timestamp
    if not pd.api.types.is_datetime64_any_dtype(cluster['apper_time']):
        return None

    # 开始执行
    need_id_list = []
    current_time = None
    for index, row in cluster.iterrows():
        # 临时时间
        temp_time = row["apper_time"]
        if current_time is None or (temp_time - current_time) > pd.Timedelta(seconds=time_window):
            need_id_list.append(index)
        current_time = temp_time

    return cluster.loc[need_id_list]


if __name__ == "__main__":
    # 读取数据
    df = pd.read_excel("./data/drop_duplicate_data.xlsx", engine='openpyxl')
    res = drop_duplicate(df)