# -*- encoding: utf-8 -*-
'''
@File    :   _13.py
@Time    :   2023/01/16 13:55:41
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   网络设备4A纳管解析函数
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero
from lib.utils.base import _get4ASSHName

# from lib.utils.base import


def GetNetwork4AWebAssetName(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    #
    df = target_data_frame

    fetched_dict = jwDict.GetDict("4A-web资产")
    _4Alist = []
    for k, v in fetched_dict.items():
        if k not in _4Alist:
            _4Alist.append(k)

    # 原始数据
    source_data = zero.GetData(source_sheet)

    # 按照字典过滤
    df[col_name] = source_data[source_data[value].isin(_4Alist)][source_column]

    return df, True


def GetNetwork4ASSHAssetIP(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    # 4A资产信息-ssh 资产ip
    df = target_data_frame

    # 原始数据
    source_data = zero.GetData(source_sheet)

    df[col_name] = pd.DataFrame(
        source_data[source_column].unique(), columns=[col_name])

    return df, True


def GetNetwork4ASSHAssetName(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    # 4A资产信息-ssh 资产名称
    df = target_data_frame

    if "资产ip" not in df.columns:
        df[col_name] = '待确认：需首先配置"资产ip"'
        return df, False

    # df[col_name] =df.apply(
    #     lambda row:
    # )
    network = zero.GetData("网络设备")
    df[col_name] = df.apply(
        lambda row: _get4ASSHName(network, row["资产ip"]), axis=1)

    return df, True
