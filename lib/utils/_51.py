# -*- encoding: utf-8 -*-
'''
@File    :   51.py
@Time    :   2023/01/08 15:07:59
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   51 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _generateProjectSiteInfo, _getProjectDictItem, _fetchSiteName, _getAssetInfo, _getRackProductLine, _fetchSiteCol, _getNetworkAssetPos, _getSNMPVersion


def SequenceNumber(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    df.insert(0, col_name, range(1, len(df)+1))

    return df, True


def SnmpTarget(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    network = zero.GetData("网络设备")[['网管网（包括iLO、ipmi）']].drop_duplicates()
    server = zero.GetData("服务器")[['网管网（包括iLO、ipmi）']].drop_duplicates()

    dfSummary = pd.concat([network, server], axis=0)

    df[col_name] = dfSummary['网管网（包括iLO、ipmi）']

    return df, True
