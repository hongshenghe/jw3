# -*- encoding: utf-8 -*-
'''
@File    :   62.py
@Time    :   2023/01/08 15:07:59
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   62云桌面服务器 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _getCloudDesktopRackAsset, _getCloudDesktopPos


def GetCloudDesktopRack(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    """获取云桌面机架位置

    Args:
        zero (JWZero): 零号表对象实例

    Returns:
        pd.DataFrame: DataFrame

    样例：
        HAZZ-202-"04-01"
        编码缩写-机房-"机架"
    """
    df = target_data_frame

    rackCode = zero.GetProject("编码缩写")
    df2 = zero.GetData(source_sheet)[
        [source_column,  '机架']]
    df2[col_name] = df2.apply(
        lambda row: _getCloudDesktopRackAsset(rackCode, row['机架']), axis=1)

    df[col_name] = df2[col_name]
    return df, True


def GetCloudDesktopPos(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    df2 = zero.GetData(source_sheet)
    df2[col_name] = df2.apply(
        lambda row: _getCloudDesktopPos(row['设备高度'], row['U位置']), axis=1)

    df[col_name] = df2[col_name]

    return df, True


def GetCloudDesktopProjectSite(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    df[col_name] = df.apply(
        lambda row: zero.GetProject("省份") + zero.GetProject("市"), axis=1)
    return df, True
