# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2023/01/07 23:01:42
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   None
'''

# 配置文件计算方法

def copy(target_data_frame, name, source_sheet_name, source_column_name, data, value, dict_info, catalog, entry):
    """复制列"""

    df = target_data_frame
    if not source_sheet_name or not source_column_name:
        df[name] = "待确认: 源sheet或源列未指定"
        return df, False

    df[name] = data[source_sheet_name][source_column_name]
    return df, True
