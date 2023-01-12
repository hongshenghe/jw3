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
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _generateProjectSiteInfo, _getProjectDictItem, _fetchSiteName, _getAsssetInfo, _getRackProductLine, _fetchSiteCol, _getNetworkAssetPos, _getSNMPVersion


def GenerateProjectSiteInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame
    df[col_name] = _generateProjectSiteInfo(zero, value)
    return df, True


def GetProjectDict(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame
    df[col_name] = df.apply(
        lambda row: _getProjectDictItem(zero, value), axis=1)
    return df, True


def SetValue(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    """设置列值为指定值"""

    df = target_data_frame
    if not value:
        df[col_name] = "待确认: 没有指定设定值"
        return df, False
    df[col_name] = value
    return df, True


def SetNone(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    """设置列值为指定值"""

    df = target_data_frame
    df[col_name] = ""
    return df, True


def GetProjectSite(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
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


def GetRackProductLine(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
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
    asserts = zero.GetData("设备清单")

    dfSummary['产品线'] = dfSummary.apply(
        lambda row: _getAsssetInfo(asserts, row['对应设备清单-配对列'], "产品线"), axis=1)

    # 获取原始机房号
    df[col_name] = _generateProjectSiteInfo(zero, "原始机房号")

    # df[col_name] = '-'
    df[col_name] = df.apply(
        lambda row: _getRackProductLine(dfSummary, "%s列%s" % (row['列号'], row['机柜号']), row[col_name]), axis=1)
    return df, True


#  self.zero, self.jwDict, df, col_name, value, source_sheet, source_column
def GetPosition(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
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


def GetAssertInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    asserts = zero.GetData("设备清单")

    # 网络设备或者服务器
    asertSheet = zero.GetData(source_sheet)

    # 生成目标列
    asertSheet[col_name] = asertSheet.apply(
        lambda row: _getAsssetInfo(asserts, row[source_column], value), axis=1)

    df[col_name] = asertSheet[col_name]
    return df, True


def GetSNMPVersion(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    # 获取品牌
    df, flag = GetAssertInfo(zero, jwDict, df, col_name,
                             value, source_sheet, source_column)

    # 获取SNMP版本字典
    snmp_dict = jwDict.GetDict("SNMP版本")

    # 获取SNMP版本
    df[col_name] = df.apply(
        lambda row: _getSNMPVersion(row[col_name], snmp_dict), axis=1)

    return df, True


# def GetNetworkAssertLevel(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

#     df = target_data_frame

#     # 获取网络设备层级字典
#     fetchedDict = jwDict.GetDict("网络设备层级")

#     return df, True
