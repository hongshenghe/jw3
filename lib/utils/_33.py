# -*- encoding: utf-8 -*-
'''
@File    :   33.py
@Time    :   2023/01/08 15:07:59
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   33 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _generateProjectSiteInfo, _getProjectDictItem, _fetchSiteName, _getAsssetInfo, _getRackProductLine, _fetchSiteCol, _getNetworkAssetPos, _getSNMPVersion


def SequenceNumber(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    # TODO 递增序号1,2,3 eg..
    return df, True


def HarvestMachine(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    # dfA = zero.GetData("网络设备")["网管网（包括iLO、ipmi）"]
    # dfB = zero.GetData("服务器")["网管网（包括iLO、ipmi）"]

    # df2[col_name] = pd.concat(dfA, dfB, ignore_index=True)

    # df[col_name] = df2[col_name]

    # TODO 合并sheet (网络设备)[网管网（包括iLO、ipmi）],(服务器)[网管网（包括iLO、ipmi）]
    return df, True
