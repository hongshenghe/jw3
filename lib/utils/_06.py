# -*- encoding: utf-8 -*-
'''
@File    :   06.py
@Time    :   2023/01/08 15:07:59
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   06 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _generateProjectSiteInfo, _getProjectDictItem, _fetchSiteName, _getAssetInfo, _getRackProductLine, _fetchSiteCol, _getNetworkAssetPos, _getSNMPVersion


def VlanAsset(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    network = zero.GetData("网络设备")[['系统名称', '网管网（包括iLO、ipmi）']]
    server = zero.GetData("服务器")[['系统名称', '网管网（包括iLO、ipmi）']]

    dfSummary = pd.concat([network, server], axis=0)

    df[col_name] = dfSummary['系统名称', '网管网（包括iLO、ipmi）']

    return df, True


def ResourceType(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    network = zero.GetData("网络设备")[['系统名称']]
    server = zero.GetData("服务器")[['系统名称']]

    dfSummary = pd.concat([network, server], axis=0)

    df[col_name] = dfSummary['系统名称']

    return df, True


def DeviceCode(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    network = zero.GetData("网络设备")[['设备标签']]
    server = zero.GetData("服务器")[['设备标签']]

    dfSummary = pd.concat([network, server], axis=0)

    df[col_name] = dfSummary['设备标签']

    return df, True


def DeviceCode(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    network = zero.GetData("网络设备")[['设备标签']]
    server = zero.GetData("服务器")[['设备标签']]

    dfSummary = pd.concat([network, server], axis=0)

    df[col_name] = dfSummary['设备标签']

    return df, True


def DeviceIP(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    network = zero.GetData("网络设备")[['网管网（包括iLO、ipmi）']]
    server = zero.GetData("服务器")[['网管网（包括iLO、ipmi）']]

    dfSummary = pd.concat([network, server], axis=0)

    df[col_name] = dfSummary['网管网（包括iLO、ipmi）']

    return df, True


def VlanAsset(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    network = zero.GetData("网络设备")[['网管网vlan']]
    server = zero.GetData("服务器")[['网管网vlan']]

    dfSummary = pd.concat([network, server], axis=0)

    df[col_name] = dfSummary['网管网vlan']

    return df, True
