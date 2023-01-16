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
