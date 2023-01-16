# -*- encoding: utf-8 -*-
'''
@File    :   base.py
@Time    :   2023/01/12 13:15:42
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   基础模块
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero


def _fetchDictValue(fetchedDict: dict, match_value: str, dict_name: str) -> str:
    """匹配字典内容

    Args:
        jwDict (JWDict): 字典对象
        match_value (str): 需要匹配的值，例如系统名称
        dict_name (str): 字典名称

    Returns:
        str: 字典的键值
    """

    for k, v in fetchedDict.items():
        if re.search(k, match_value):
            return v

    if "其他" in fetchedDict:
        return fetchedDict['其他']

    return "待确认: %s字典无法匹配到:%s" % (dict_name, match_value)


def _fetchSiteName(siteName, roomid):
    return siteName.replace("{site_name}", str(roomid))


def _fetchSiteCol(rack, pos):
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
    df2["机房"] = df2.apply(lambda row: _fetchSiteName(
        siteName, row['机房']), axis=1)
    df2["列号"] = df2.apply(lambda row: _fetchSiteCol(row['机架'], 0), axis=1)
    df2["机柜号"] = df2.apply(lambda row: _fetchSiteCol(row['机架'], 1), axis=1)

    temp = df2[['机房', '列号', '机柜号', '原始机房号']].drop_duplicates()

    return temp[key_col]


def _getProjectDictItem(zero, key: str) -> str:
    content = zero.GetProject(key)
    # print("key:%s value:%s" % (key, content))
    return content


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


def _getNetworkAssetPos(site_name: str, room_id: str, rack_info: str, start_pos: str, height: str) -> str:

    # 机房
    full_site_name = _fetchSiteName(site_name, room_id)

    # 列号
    rack_col = _fetchSiteCol(rack_info, 0)
    # logging.info("列号:%s" % rack_col)

    # 机柜号
    rack_no = _fetchSiteCol(rack_info, 1)
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


def _getSNMPVersion(brand: str, snmp_dict: dict) -> str:
    for k, v in snmp_dict.items():
        if k == brand:
            return v
    if '其他' in snmp_dict:
        return snmp_dict['其他']
    return '待确认: 请检查SNMP版本字典，无默认"其他"的内容'


def _getNetworkLogicCode(group_name: str, asset_label: str) -> str:
    """获取网络设备逻辑编码

    Args:
        group_name (str): 堆叠名称
        asset_label (str): 设备标签

    Returns:
        str: 逻辑编码 
    """
    _group = str(group_name)

    code = _group
    if pd.isna(group_name):
        code = asset_label

    # print("-------------堆叠名称：%s 设备标签：%s 逻辑编码:%s" % (_group, asset_label, code))
    return code