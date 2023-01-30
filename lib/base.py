# -*- encoding: utf-8 -*-
'''
@File    :   base.py
@Time    :   2023/01/07 22:06:20
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   None
'''

# 内部调用公共模块
import openpyxl
import os
import uuid


def fetchExcelSheets(fileName: str) -> list:
    """获取excel文件sheet列表

    Args:
        fileName (str): _description_

    Returns:
        list: _description_
    """
    wb = openpyxl.load_workbook(fileName)
    return wb.sheetnames 


def ensurePath(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return


def generate_batchid() -> str:
    return str(uuid.uuid1())


def fetch_file_path(work_home: str, dir_name: str, file_name: str) -> str:
    return os.path.join(work_home, dir_name, file_name)


def fetch_dict_file_name(work_home: str, dict_file_name: str) -> str:
    return fetch_file_path(work_home, "upload", dict_file_name)


def fetch_zero_file_name(work_home: str, zero_file_name: str) -> str:
    return fetch_file_path(work_home, "upload", zero_file_name)


def fetch_down_dir(work_home: str) -> str:
    return fetch_file_path(work_home, "down")
