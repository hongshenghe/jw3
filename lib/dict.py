# -*- encoding: utf-8 -*-
'''
@File    :   dict.py
@Time    :   2023/01/07 18:10:14
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   None
'''

# 字典

import pandas as pd
import openpyxl
import os

from lib.base import fetch_dict_file_name, fetchExcelSheets
from lib.logger import logging


class JWDict(object):
    # 字典处理类

    # 工作目录
    _work_dir = ""

    # 字典文件
    _dict_file = ""

    # 字典配置规则
    DICT_RULE_CONFIGS = {
        # "字典名称":[sheet名称，key字段名称，：字段列表]
        "原厂售后电话": ["原厂售后电话", "厂商名称", "热线电话"],
        "品牌字典表": ["品牌字典表", "型号", "厂商名称"],

        "功耗表": ["功耗表", "类别", "实际功率(W)"],
        "资产原值表": ["资产原值", "系统名称", "资产原值（除税价）"],
    }

    # 字典存储容器
    # 结构:
    # data = {
    #     "字典名称1": {
    #         "key1": "value",
    #         "key2": "value",
    #         "key3": "value",
    #         },
    #     "字典名称2": {
    #         "key1": "value",
    #         "key2": "value",
    #         "key3": "value",
    #         },
    # }
    data = {}
    manufacturer_data = {}

    def __init__(self, work_dir: str, dict_file: str) -> None:
        """字典初始化

        Args: 
            work_dir (str): 工作目录
            dict_file (str): 字典表数据文件名称
        """
        self._work_dir = work_dir
        self._dict_file = dict_file

        # 初始化字典表
        self.data = self._init_dict()

        # 初始化设备维保信息
        self._loadDataFrame("设备维保")

    def _init_dict(self) -> dict:
        """初始化字典表

        Returns:
            dict: 字典实例

        # 字典结构:
        #     {
        #       "品牌":
        #          {
        #           "HW": "华为",
        #           "ZX": "中兴",
        #           "CJB": "超聚变",
        #          },
        #     }
        """

        df = pd.read_excel(self._dict_file,
                           sheet_name="字典表", engine='openpyxl')
        dict_data = {}
        for i, row in df.iterrows():

            # 分类
            catalog = row[0]

            # 条目
            entity = row[1]

            # 内容
            value = row[2]

            if catalog not in dict_data:
                dict_data[catalog] = {}

            if entity not in catalog:
                dict_data[catalog][entity] = {}

            dict_data[catalog][entity] = value

        # project_info = self._load_project_info()
        # dict_data["项目"] = self._load_project_info()
        return dict_data

    def Get(self, dict_name: str, key: str) -> str:
        """获取键值

        Args:
            dict_name (str): 字典名称
            key (str): 键

        Returns:
            str: 键值
        """
        if dict_name not in self.data:
            return "待确认: 字典文件不存在该字典名称:%s" % dict_name
        if key not in self.data[dict_name]:
            return "待确认: 字典文件%s字典不存在该键值:%s" % (dict_name, key)

        return self.data[dict_name][key]

    def GetDict(self, dict_name: str) -> dict:
        """获取字典

        Args:
            dict_name (str): 字典名称

        Returns:
            dict: 字典对象
        """
        # logging.warning("获取字典:%s" % dict_name)

        fetchedDict = {}
        if dict_name not in self.data:
            return fetchedDict
        fetchedDict = self.data[dict_name]

        # logging.warning("获取字典内容:%s" % fetchedDict)
        # for k, v in fetchedDict.items():
        #     logging.warning("k:%s v:%s" % (k, v))

        return fetchedDict

    def _check_sheet_name(self, sheet_name: str) -> bool:
        """检查sheet_name是否存在

        Args:
            sheet_name (str): sheet名称

        Returns:
            bool: 是否存在
        """
        self.sheet_list = self._fetch_sheet_list(
            os.path.join(self._work_dir, self._dict_file))

        return sheet_name in self.sheet_list

    def LoadSheets(self) -> Exception:
        """加载sheet

        Returns:
            Exception: _description_
        """
        self.sheet_list = self._fetch_sheet_list(
            os.path.join(self._work_dir, self._dict_file))
        return None

    def _fetch_sheet_list(self, fileName: str) -> list:
        """获取excel文件sheet列表

        Args:
            fileName (str): _description_

        Returns:
            list: _description_
        """
        # wb = openpyxl.load_workbook(fileName)
        # sheet_list = wb.get_sheet_names()

        # return sheet_list
        return fetchExcelSheets(fileName)

    def FetchManufacturerInfo(self, vendor: str, asset_type: str, column_name: str) -> str:

        # print("vendor:%s asset_type:%s column_name:%s" %
        #       (vendor, asset_type, column_name))

        df = self.manufacturer_data['设备维保']
        # print(df.columns)

        df = df[df["厂家"] == vendor]
        df = df[df["设备类型"] == asset_type]

        # df = df[((df["厂家"] == vendor) & (df["设备类型"] == asset_type))]

        if len(df) == 0:
            return "待确认：无匹配的维保信息，厂家：%s 设备类型：%s 查找列名称：%s" % (vendor, asset_type,  column_name)

        if column_name not in df.columns:
            return "待确认：维保信息不存在需要的列:%s，厂家：%s 设备类型：%s 查找列名称：%s" % (column_name, vendor, asset_type,  column_name)

        try:
            resp = str(df.reset_index()[column_name][0])
        except Exception as ex:
            resp = "待确认：无匹配的维保信息，厂家：%s 设备类型：%s 查找列名称：%s 异常信息:%s" % (
                vendor, asset_type,  column_name, str(ex))
        return resp

    def _loadDataFrame(self, data_name: str) -> Exception:
        if data_name not in self.data:
            self.data[data_name] = None

        # data sheet 是否存在
        if not self._check_sheet_name(data_name):
            return Exception("Error:%s 表格不存在" % data_name)

        # 加载sheet
        _dict_file_name = os.path.join(self._work_dir, self._dict_file)

        df = pd.read_excel(
            _dict_file_name, sheet_name=data_name, engine='openpyxl')

        self.manufacturer_data[data_name] = df
        return None
