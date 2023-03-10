# -*- encoding: utf-8 -*-
'''
@File    :   _52.py
@Time    :   2023/01/16 13:55:41
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   52 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _fetchDictValue


def GetVMHostInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    fetched_dict = jwDict.GetDict("采集机信息收纳")
    _vmHostInfo = []
    for k, v in fetched_dict.items():
        if k not in _vmHostInfo:
            _vmHostInfo.append(k)

    # 原始数据
    source_data = zero.GetData(source_sheet)

    # 按照字典过滤
    df[col_name] = source_data[source_data[value].isin(
        _vmHostInfo)][source_column]

    return df, True


def GetVMInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):

    df = target_data_frame

    fetched_dict = jwDict.GetDict("虚拟机信息")
    _vmInfo = []
    for k, v in fetched_dict.items():
        if k not in _vmInfo:
            _vmInfo.append(k)

    # 原始数据
    source_data = zero.GetData(source_sheet)

    # 按照字典过滤
    df[col_name] = source_data[source_data[value].isin(_vmInfo)][source_column]

    return df, True

# 暂时不使用
# def GetVMInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str,filter:dict):
#     """获取虚拟机信息

#     Args:
#         zero (_type_): 零号表对象实例
#         target_data_frame (_type_): 生成数据集合

#     Returns:
#         _type_: DataFrame
#     """
#     df = target_data_frame

#     fetched_dict = jwDict.GetDict("采集机信息收纳")
#     _vm = []
#     for k, v in fetched_dict.items():
#         if k not in _vm:
#             _vm.append(k)

#     vminfo = zero.GetData("VM规划")

#     server_data = zero.GetData("服务器")
#     server_data = server_data[server_data["角色"].isin(_vm)][['角色', '设备标签']]

#     df[col_name] = server_data.apply(
#         lambda row: _getvminfo(vminfo, row["设备标签"], value), axis=1)

#     return df, True
