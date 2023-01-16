# -*- encoding: utf-8 -*-
'''
@File    :   12.py
@Time    :   2023/01/08 15:07:59
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   12 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _generateProjectSiteInfo, _getProjectDictItem, _fetchSiteName, _getAsssetInfo, _getRackProductLine, _fetchSiteCol, _getNetworkAssetPos, _getSNMPVersion


def GetDataCenterShort(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame

    df[col_name] = df.apply(
        lambda row: zero.GetProject("编码缩写") + zero.GetProject("资源编码"), axis=1)

    return df, True


def BMC(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame

    df[col_name] = df.apply(
        lambda row: 'BMC-' + zero.GetProject("资源池") + '-' + zero.GetProject("省份") + zero.GetProject("市"), axis=1)

    return df, True


def HTTPS(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame

    df[col_name] = "https://" + zero.GetData("服务器")["网管网（包括iLO、ipmi）"]
    return df, True
