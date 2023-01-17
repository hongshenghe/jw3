# -*- encoding: utf-8 -*-
'''
@File    :   _07.py
@Time    :   2023/01/17 11:06:12
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   07表使用函数
'''
import re

import pandas as pd

from lib.dict import JWDict
from lib.logger import logging
from lib.zero import JWZero


def CopySheet(zero: JWZero, jwDict: JWDict, target_data_frame, col_name: str, value: str, source_sheet: str, source_column: str):
    df = target_data_frame
    df = zero.GetData(source_sheet)
    return df, True
