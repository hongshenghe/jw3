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


def fetchSiteName(siteName, roomid):
    return siteName.replace("{site_name}", str(roomid))


def fetchSiteCol(rack, pos):
    # rack = row['机架']  # 04列01
    m = re.match("(\S+)列(\S+)$", rack)
    if m:
        return m.groups()[pos]
    m = re.match("(\S+)-(\S+)$", rack)
    if m:
        return m.groups()[pos]
    return "待确认: 无法获取机架信息，机架格式应为:04列01，当前值:%s" % rack


def _generateProjectSiteInfo(zero: JWZero, key_col: str) -> pd.DataFrame:
    """生成机房相关信息

    Args:
        zero (JWZero): 零号表实例
        key_col (str): 返回的列名称

    Returns:
        _type_: pd.DataFrame
    """
    siteName = zero.GetProject("云调所属机房")
    network = zero.GetData("网络设备")[['机架', '机房']].drop_duplicates()
    server = zero.GetData("服务器")[['机架', '机房']].drop_duplicates()

    df2 = pd.concat([network, server], axis=0).sort_values(
        by=['机架', '机房'], ascending=True)
    df2["原始机房号"] = df2['机房']
    df2["机房"] = df2.apply(lambda row: fetchSiteName(
        siteName, row['机房']), axis=1)
    df2["列号"] = df2.apply(lambda row: fetchSiteCol(row['机架'], 0), axis=1)
    df2["机柜号"] = df2.apply(lambda row: fetchSiteCol(row['机架'], 1), axis=1)

    temp = df2[['机房', '列号', '机柜号', '原始机房号']].drop_duplicates()

    return temp[key_col]


def GenerateProjectSiteInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame
    df[col_name] = _generateProjectSiteInfo(zero, value)
    return df, True


def getProjectDictItem(zero, key: str) -> str:
    content = zero.GetProject(key)
    # print("key:%s value:%s" % (key, content))
    return content


def GetProjectDict(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame
    df[col_name] = df.apply(
        lambda row: getProjectDictItem(zero, value), axis=1)
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
    df[col_name] = df.apply(lambda row: fetchSiteName(
        siteName, row[col_name]), axis=1)

    return df, True


def _getAsssetInfo(asserts: pd.DataFrame, match_col: str, parameter: str) -> str:
    """获取资产信息表格的列属性

    Args:
        asserts (pd.DataFrame): 资产dataframe对象
        match_col (str): 子表配队列
        parameter (str): 资产信息表格的列名称

    Returns:
        str: _description_
    """
    df = asserts[asserts['配对列'] == match_col][parameter]
    if len(df) == 0:
        return "待确认: 请核对是否存在 %s 配对列,设备信息是否存在%s列" % (match_col, parameter)
    return df.iloc(0)[0]


def _getRackProductLine(rackSummary: pd.DataFrame, rack: str, site: str) -> str:

    # df = rackSummary[rackSummary['机架'] ==
    #                  rack & rackSummary['机房'] == site]

    df = rackSummary[(rackSummary['机架'] == rack) & (rackSummary['机房'] == site)]

    if len(df) == 0:
        return "待确认: 无法获取机柜产品线，需核对是否存在%s机房%s机架" % (site, rack)

    group = df.groupby(['产品线'])['产品线'].count()
    productMax = group[0]
    productMaxID = 0
    for idx in range(0, len(group)):
        if group[idx] > productMax:
            productMax = group[idx]
            productMaxID = idx

    return group.index[productMaxID]


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


def getNetworkAssetPos(site_name: str, room_id: str, rack_info: str, start_pos: str, height: str) -> str:

    # logging.info("siteName:%s" % site_name)
    # logging.info("room_id:%s" % room_id)
    # logging.info("rack_info:%s" % rack_info)
    # logging.info("start_pos:%s" % start_pos)
    # logging.info("heigh:%s" % height)

    # 机房
    full_site_name = fetchSiteName(site_name, room_id)

    # 列号
    rack_col = fetchSiteCol(rack_info, 0)
    # logging.info("列号:%s" % rack_col)

    # 机柜号
    rack_no = fetchSiteCol(rack_info, 1)
    # logging.info("机柜号:%s" % rack_no)

    # 起始位置
    rack_start_pos = int(re.search("(\d+)", str(start_pos)).groups()
                         [0]) if re.search("(\d+)", str(start_pos)) else 0
    # 设备高度
    asset_height = int(height) if not pd.isna(height) else 0

    # 设备位置
    asset_pos = rack_start_pos if asset_height == 1 else "%s~%s" % (
        rack_start_pos, rack_start_pos+asset_height-1)

    physical_address = "%s/%s列%s(%s)" % (full_site_name,
                                         rack_col, rack_no, asset_pos)
    return physical_address


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
    df2[col_name] = df2.apply(lambda row: getNetworkAssetPos(
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


def _getSNMPVersion(brand: str, snmp_dict: dict) -> str:
    for k, v in snmp_dict.items():
        if k == brand:
            return v
    if '其他' in snmp_dict:
        return snmp_dict['其他']
    return '待确认: 请检查SNMP版本字典，无默认"其他"的内容'


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



def GetNetworkAssertLevel(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame
    
    # 获取网络设备层级字典
    fetchedDict = jwDict.GetDict("网络设备层级")

    return df,True