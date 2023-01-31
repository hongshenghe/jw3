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
from lib.utils.base import _get4ASSHName, _getNetworkInfoColumnByIP, _getAssetInfoByNetworkIP, _getDictByNetworkIP


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

    network = zero.GetData("网络设备")
    _ip_groups = network["网管网（包括iLO、ipmi）"].value_counts(
        ascending=True).reset_index()
    _ip_groups.columns = ["ip", "cnt"]
    
    df[col_name] = df.apply(
        lambda row: _get4ASSHName(network, row["资产ip"], _ip_groups), axis=1)

    return df, True


def GetNetworkColumnBy4ASSHAssetIP(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    # 根据ip地址获取网络设备表中对应列的信息
    df = target_data_frame

    if "资产ip" not in df.columns:
        df[col_name] = '待确认：需首先配置"资产ip"列'
        return df, False

    network = zero.GetData("网络设备")
    col_name = value
    df[col_name] = df.apply(
        lambda row: _getNetworkInfoColumnByIP(network=network, ip=row["资产ip"], column_name=col_name), axis=1)

    return df, True


def GetAssetInfoByNetworkIP(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    # 根据ip地址获取网络设备的资产清单信息

    df = target_data_frame

    if "资产ip" not in df.columns:
        df[col_name] = '待确认：需首先配置"资产ip"列'
        return df, False

    assets = zero.GetData("设备清单")
    network = zero.GetData("网络设备")
    col_name = value

    df[col_name] = df.apply(lambda row: _getAssetInfoByNetworkIP(
        assets=assets, network=network, ip=row["资产ip"], column_name=col_name), axis=1)

    return df, True


def GetDictByNetworkIP(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    # 根据ip地址获取网络设备的资产清单信息

    df = target_data_frame

    if "资产ip" not in df.columns:
        df[col_name] = '待确认：需首先配置"资产ip"列'
        return df, False

    network = zero.GetData("网络设备")

    # 匹配字典
    dict_name = value
    fetchedDict = jwDict.GetDict(dict_name)

    network_property_name = source_column
    df[col_name] = df.apply(lambda row: _getDictByNetworkIP(
        network=network, ip=row["资产ip"], match_column_name=network_property_name, fetched_dict=fetchedDict, dict_name=dict_name), axis=1)

    return df, True
