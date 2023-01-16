# -*- encoding: utf-8 -*-
'''
@File    :   15.py
@Time    :   2023/01/08 15:07:59
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   15 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _generateProjectSiteInfo, _getProjectDictItem, _fetchSiteName, _getAsssetInfo, _getRackProductLine, _fetchSiteCol, _getNetworkAssetPos, _getSNMPVersion


def PrometheusSNMPServer(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    df[col_name] = df.apply(
        lambda row: zero.GetProject("SNMP/NTP-1") + "\r\n" + zero.GetProject("SNMP/NTP-2"), axis=1)
    # our_database[new_column] = "\n".join([list of columns you want])
    return df, True


def PrometheusFilter(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    fetched_dict = jwDict.GetDict("普罗米修斯")
    _Prometheu = []
    for k, v in fetched_dict.items():
        if k not in _Prometheu:
            _Prometheu.append(k)

    # 原始数据
    source_data = zero.GetData(source_sheet)

    # 按照字典过滤
    df[col_name] = source_data[source_data[value].isin(
        _Prometheu)][source_column]

    return df, True