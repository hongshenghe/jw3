# -*- encoding: utf-8 -*-
'''
@File    :   05.py
@Time    :   2023/01/08 15:07:59
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   05 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.zero import JWZero
from lib.utils.base import _fetchDictValue, _getAsssetInfo


def Copy(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame
    if not source_sheet or not source_sheet:
        df[col_name] = "待确认: 源sheet或源列未指定"
        return df, False

    df[col_name] = zero.GetData(source_sheet)[source_column]
    return df, True


def GetDict(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame
    if not source_sheet or not source_column or not col_name or not value:
        df[col_name] = "待确认: GetDict需要指定source_sheet、source_column、value、col_name"
        return df, False

    # 获取原始值
    df[col_name] = zero.GetData(source_sheet)[[source_column]]

    # 匹配字典
    fetchedDict = jwDict.GetDict(value)

    df[col_name] = df.apply(
        lambda row: _fetchDictValue(fetchedDict, row[col_name], value), axis=1)
    return df, True


def GetSubProductLine(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    """获取细分产品线

    Args:
        zero (_type_): 零号表实例 
    Returns:
        _type_: pd.DataFrame
    """

    df = target_data_frame

    asserts = zero.GetData("设备清单")

    # 获取细分产品线字典
    sub_product_dict = jwDict.GetDict("细分产品线")

    # 生成原始数据
    source_data = zero.GetData(source_sheet)

    # 生成产品线
    df[col_name] = source_data.apply(
        lambda row: _getAsssetInfo(asserts, row[source_column], "产品线"), axis=1)

    # 生成细分产品线
    df[col_name] = df.apply(
        lambda row: _fetchDictValue(sub_product_dict, row[col_name], "细分产品线"), axis=1)

    return df, True


def GetNetworkLogicCode(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    """获取网络设备逻辑编码
    返回源数据“堆叠后名称/M-LAG（逻辑名称）”
    如果为空，则返回“设备标签“
    """

    df = target_data_frame

    # if pd.isna(df[col_name]):
    # df[col_name] = zero.GetData("网络设备")["堆叠后名称/M-LAG（逻辑名称）"]
    # else:
    # df[col_name] == zero.GetData("网络设备")["堆叠后名称/M-LAG（设备标签）"]
    # TODO：待确认

    return df, False
