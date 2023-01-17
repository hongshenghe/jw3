# -*- encoding: utf-8 -*-
'''
@File    :   _52.py
@Time    :   2023/01/16 13:55:41
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   52 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

# from lib.utils.base import


def SnmpHostInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    fetched_dict = jwDict.GetDict("采集机信息收纳")
    _vmHost = []
    for k, v in fetched_dict.items():
        if k not in _vmHost:
            _vmHost.append(k)

    # 原始数据
    source_data = zero.GetData(source_sheet)

    # 按照字典过滤
    df[col_name] = source_data[source_data[value].isin(_vmHost)][source_column]

    return df, True


def VmInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    print("source_sheet:%s" % source_sheet)
    print("source_column:%s" % source_column)
    print("value:%s" % value)

    df = target_data_frame

    fetched_dict = jwDict.GetDict("采集机配置")
    _vm = []
    for k, v in fetched_dict.items():
        if k not in _vm:
            _vm.append(k)

    # 原始数据
    source_data = zero.GetData(source_sheet)

    # 按照字典过滤
    df[col_name] = source_data[source_data[value].isin(_vm)][source_column]

    return df, True


def GetvmInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    """获取机柜所属产品线

    Args:
        zero (_type_): 零号表对象实例
        target_data_frame (_type_): 生成数据集合 

    Returns:
        _type_: DataFrame
    """
    df = target_data_frame

    server = zero.GetData("服务器")[['角色', '设备标签'] == 'KVM']

    dfSummary = pd.concat([network, server], axis=0).sort_values(
        by=['对应设备清单-配对列', '机架', '机房'], ascending=True)

    # assert_list = 产品线
    asserts = zero.GetData("设备清单")

    dfSummary['产品线'] = dfSummary.apply(
        lambda row: _getAsssetInfo(asserts, row['对应设备清单-配对列'], "产品线"), axis=1)

    # 获取原始机房号
    df[col_name] = _generateProjectSiteInfo(zero, "原始机房号")

    # df[col_name] = '-'
    df[col_name] = df.apply(
        lambda row: _getRackProductLine(dfSummary, "%s列%s" % (row['列号'], row['机柜号']), row[col_name]), axis=1)
    return df, True
