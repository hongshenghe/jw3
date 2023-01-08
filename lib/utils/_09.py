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


def Copy(zero, target_data_frame, col_name, value, source_sheet):
    df = target_data_frame
    if not source_sheet or not source_sheet:
        df[col_name] = "待确认: 源sheet或源列未指定"
        return df, False

    df[col_name] = zero.GetData(source_sheet)[value]
    return df, True
