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
import sys

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _fetchDictValue, _generateProjectSiteInfo, _getProjectDictItem, _fetchSiteName, _getAssetInfo, _getRackProductLine, _fetchSiteCol, _getNetworkAssetPos, _getSNMPVersion
from lib.utils.base import _fetch_dict_key


def GenerateProjectSiteInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):

    df = target_data_frame
    df[col_name] = _generateProjectSiteInfo(zero, value)
    return df, True


def GetProjectDict(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):
    df = target_data_frame
    df[col_name] = df.apply(
        lambda row: _getProjectDictItem(zero, value), axis=1)
    return df, True


def SetValue(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):
    """设置列值为指定值"""

    df = target_data_frame
    if not value:
        df[col_name] = "待确认: 没有指定设定值"
        return df, False

    # print("value:%s" % value)
    df[col_name] = str(value)

    return df, True


def SetNone(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):
    """设置列值为指定值"""

    df = target_data_frame
    df[col_name] = ""
    return df, True


def GetProjectSite(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):
    """获取项目机房信息列

    Args:
        zero (_type_): 零号表对象
        jwDict (_type_): 字典表对象
        target_data_frame (_type_): 生成数据集合
        col_name (_type_): 生成列的名称
        value (_type_): 不参与计算
        source_sheet (_type_): 网络设备或者服务器
        source_column (_type_): 网络设备、服务器sheet的“机房”

    Returns:
        _type_: dataframe
    """
    df = target_data_frame

    siteName = zero.GetProject(value)
    df[col_name] = zero.GetData(source_sheet)[source_column]
    df[col_name] = df.apply(lambda row: _fetchSiteName(
        siteName, row[col_name]), axis=1)

    return df, True


def GetRackProductLine(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):
    """获取机柜所属产品线

    Args:
        zero (_type_): 零号表对象实例
        target_data_frame (_type_): 生成数据集合 

    Returns:
        _type_: DataFrame
    """
    df = target_data_frame

    network = zero.GetData("网络设备")[['对应设备清单-配对列', '机架', '机房']]
    server = zero.GetData("服务器")[['对应设备清单-配对列', '机架', '机房']]

    dfSummary = pd.concat([network, server], axis=0).sort_values(
        by=['对应设备清单-配对列', '机架', '机房'], ascending=True)

    # assert_list = 产品线
    assets = zero.GetData("设备清单")

    dfSummary['产品线'] = dfSummary.apply(
        lambda row: _getAssetInfo(assets, row['对应设备清单-配对列'], "产品线"), axis=1)

    # 获取原始机房号
    df[col_name] = _generateProjectSiteInfo(zero, "原始机房号")

    # df[col_name] = '-'
    df[col_name] = df.apply(
        lambda row: _getRackProductLine(dfSummary, "%s列%s" % (row['列号'], row['机柜号']), row[col_name]), axis=1)
    return df, True


#  self.zero, self.jwDict, df, col_name, value, source_sheet, source_column
def GetPosition(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):
    """获取物理位置

    Args:
        zero (JWZero): 零号表对象实例

    Returns:
        pd.DataFrame: DataFrame

    样例：
        郑州市高新区枢纽楼数据中心122机房/04列01(6~17)
        郑州市高新区枢纽楼数据中心122机房/04列01(40)
    """
    df = target_data_frame

    siteName = zero.GetProject("云调所属机房")
    df2 = zero.GetData(source_sheet)[
        [source_column,  '机架', 'U位置', '设备高度']]
    df2[col_name] = df2.apply(lambda row: _getNetworkAssetPos(
        siteName, row['机房'], row['机架'], row['U位置'], row['设备高度']), axis=1)

    df[col_name] = df2[col_name]
    return df, True


def GetAssetInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):
    """获取设备信息

    Args:
        zero (JWZero): 零号文件对象实例
        jwDict (JWDict): 字典对象实例
        target_data_frame (_type_): 目标df
        col_name (str): 列名称
        value (str): _description_
        source_sheet (str): 源表格
        source_column (str): 源列

    Returns:
        _type_: df
    """

    df = target_data_frame

    asserts = zero.GetData("设备清单")

    # 网络设备或者服务器
    source_data = zero.GetData(source_sheet)
    if filter:
        if filter['type'] == "dict_key":
            dict_name = filter['dict_name']
            filer_column = filter['column']
            _filter_key_list = _fetch_dict_key(
                jwDict=jwDict, dict_name=dict_name)
            source_data = source_data[source_data[filer_column].isin(
                _filter_key_list)][source_column]

    # 生成目标列
    source_data[col_name] = source_data.apply(
        lambda row: _getAssetInfo(asserts, row[source_column], value), axis=1)

    df[col_name] = source_data[col_name]
    return df, True


def GetSNMPVersion(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):

    df = target_data_frame

    # 获取品牌
    df, flag = GetAssetInfo(zero, jwDict, df, col_name,
                            value, source_sheet, source_column)

    # 获取SNMP版本字典
    snmp_dict = jwDict.GetDict("SNMP版本")

    # 获取SNMP版本
    df[col_name] = df.apply(
        lambda row: _getSNMPVersion(row[col_name], snmp_dict), axis=1)

    # sys.exit(1)

    return df, True


def GetRackHeight(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str, filter: dict):

    df = target_data_frame

    # 获取原始值
    source_data = str(zero.GetProject("机柜机位数"))

    # 匹配字典
    fetchedDict = jwDict.GetDict(value)

    df[col_name] = df.apply(
        lambda row: _fetchDictValue(fetchedDict, source_data, value), axis=1)
    return df, True

# def GetNetworkAssertLevel(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

#     df = target_data_frame

#     # 获取网络设备层级字典
#     fetchedDict = jwDict.GetDict("网络设备层级")

#     return df, True
