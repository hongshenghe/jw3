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


def Copy(zero, jwDict: JWDict,  target_data_frame, col_name, value, source_sheet, source_column):
    df = target_data_frame
    if not source_sheet or not source_sheet:
        df[col_name] = "待确认: 源sheet或源列未指定"
        return df, False

    df[col_name] = zero.GetData(source_sheet)[source_column]
    return df, True


def fetchDictValue(fetchedDict: dict, match_value: str, dict_name: str) -> str:
    """匹配字典内容

    Args:
        jwDict (JWDict): 字典对象
        match_value (str): 需要匹配的值，例如系统名称
        dict_name (str): 字典名称

    Returns:
        str: 字典的键值
    """

    for k, v in fetchedDict.items():
        if re.search(k, match_value):
            return v

    if "其他" in fetchedDict:
        return fetchedDict['其他']

    return "待确认: %s字典无法匹配到:%s" % (dict_name, match_value)


def GetDict(zero, jwDict,  target_data_frame, col_name, value, source_sheet, source_column):
    df = target_data_frame
    if not source_sheet or not source_column or not col_name or not value:
        df[col_name] = "待确认: GetDict需要指定source_sheet、source_column、value、col_name"
        return df, False

    # 获取原始值
    df[col_name] = zero.GetData(source_sheet)[[source_column]]

    # 匹配字典
    fetchedDict = jwDict.GetDict(value)

    df[col_name] = df.apply(
        lambda row: fetchDictValue(fetchedDict, row[col_name], value), axis=1)
    return df, True
