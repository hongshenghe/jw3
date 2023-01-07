# -*- encoding: utf-8 -*-
'''
@File    :   base.py
@Time    :   2023/01/07 22:06:20
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   None
'''

# 内部调用公共模块
import openpyxl


def fetchExcelSheets(fileName: str) -> list:
    """获取excel文件sheet列表

    Args:
        fileName (str): _description_

    Returns:
        list: _description_
    """
    wb = openpyxl.load_workbook(fileName)
    sheet_list = wb.get_sheet_names()
    return sheet_list
