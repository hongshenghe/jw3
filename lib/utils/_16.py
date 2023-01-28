# -*- encoding: utf-8 -*-
'''
@File    :   15.py
@Time    :   2023/01/08 15:07:59
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   16 规则文件处理
'''

import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero

from lib.utils.base import _getMaintenanceInfo, _fetchShortSiteName


def GetMaintenanceInfo(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    df[col_name] = _getMaintenanceInfo(zero, value)

    return df, True


def GetShortSiteName(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):

    df = target_data_frame

    siteName = zero.GetProject("云调所属机房")
    _siteName = _fetchShortSiteName(siteName)

    print("_siteName:%s" % _siteName)
    df[col_name] = _siteName

    return df, True
