# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2023/01/07 23:01:42
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   配置文件计算方法
'''


import re

import pandas as pd

# def copy(target_data_frame, name, source_sheet_name, source_column_name, data, value, dict_info, catalog, entry):
#     """复制列"""

#     df = target_data_frame
#     if not source_sheet_name or not source_column_name:
#         df[name] = "待确认: 源sheet或源列未指定"
#         return df, False

#     df[name] = data[source_sheet_name][source_column_name]
#     return df, True


def fetchSiteName(siteName, row):
    return siteName.replace("{site_name}", str(row['机房']))


def fetchSiteCol(row, pos): 
    rack = row['机架']  # 04列01
    m = re.match("(\S+)列(\S+)$",rack)
    if m:
        return m.groups()[pos]
    return "待确认: 无法获取机架信息，机架格式应为:04列01，当前值:%s" % rack


def GenerateProjectSiteInfo(zero, target_data_frame, col_name, value):
    df = target_data_frame

    network = zero.GetData("网络设备")[['机架', '机房']]
    server = zero.GetData("服务器")[['机架', '机房']]
    siteName = zero.GetProject("云调所属机房")

    # 返回结果
    # dataframe ,['机房','列号','机柜号']

    network = zero.GetData("网络设备")[['机架', '机房']].drop_duplicates()
    server = zero.GetData("服务器")[['机架', '机房']].drop_duplicates()
    siteName = zero.GetProject("云调所属机房")

    df2 = pd.concat([network, server], axis=0).sort_values(
        by=['机架', '机房'], ascending=True)
    df2["机房"] = df2.apply(lambda row: fetchSiteName(siteName, row), axis=1)
    df2["列号"] = df2.apply(lambda row: fetchSiteCol(row, 0), axis=1)
    df2["机柜号"] = df2.apply(lambda row: fetchSiteCol(row, 1), axis=1)

    # d = pd.DataFrame()
    # d = pd.DataFrame(col_name, columns=[value])
    df[col_name] = df2[value]
    return df, True
