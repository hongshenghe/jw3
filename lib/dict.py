# -*- encoding: utf-8 -*-
'''
@File    :   dict.py
@Time    :   2023/01/07 18:10:14
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   None
'''

# 字典

import pandas as pd
import openpyxl
import os


class JWDict(object):
    # 字典处理类

    _zero_file_name = ""
    _work_dir = ""
    project = None
    sheet_list = []

    # 字典配置规则
    DICT_RULE_CONFIGS = {
        # "字典名称":[sheet名称，key字段名称，：字段列表]
        "原厂售后电话": ["原厂售后电话", "厂商名称", "热线电话"],
        "品牌字典表": ["品牌字典表", "型号", "厂商名称"],

        "功耗表": ["功耗表", "类别", "实际功率(W)"],
        "资产原值表": ["资产原值", "系统名称", "资产原值（除税价）"],
    }

    # 字典存储容器
    # 格式:
    # data = {
    #     "项目信息": {
    #         "项目名称": "中国电信天翼云2022年河南省业务上云资源池建设工程",
    #         "项目编号": "22HQ000726001",
    #         "投资类型": "云公司投资",
    #         "资源池": "郑州3",
    #         "省份": "河南",
    #         "市": "郑州",
    #         "工期": "1期",
    #         "设备到货时间":	"2022-11-10",
    #         "编码缩写":	"HAZZ",
    #         "SNMP/NTP-1":	"10.13.1.136",
    #         "SNMP/NTP-2":	"10.13.1.137",
    #         "云调所属机房":	"郑州市高新区枢纽楼数据中心{setname}机房",
    #         "机柜机位数":	"48",
    #         "电力输入形式":	"双路UPS",
    #         "机柜规格（A）":	"20 ",
    #         "PDU总容量":	"32",
    #         "机柜功率":	"4.8KW",
    #     },
    #     "设备清单": "dataframe",
    #     "网络设备": "dataframe",
    #     "服务器": "dataframe",
    #     "原厂售后电话": "dataframe",
    #     "品牌字典表": "dataframe",
    #     "功耗表": "dataframe",
    #     "资产原值表": "dataframe",
    # }
    data = {}

    def __init__(self, work_dir: str, zero_file: str) -> None:
        """字典初始化

        Args: 
            work_dir (str): 工作目录
            zero_file (str): 零号数据文件名称
        """
        self._work_dir = work_dir
        self._zero_file_name = zero_file

    def LoadProject(self) -> Exception:
        sheet_name = "项目信息"
        if sheet_name not in self.data:
            self.data[sheet_name] = {}

        # 加载sheet
        df = pd.read_excel(os.path.join(
            self._work_dir, self._zero_file_name), sheet_name=sheet_name, engine='openpyxl')
        for i, row in df.iterrows():
            item = row[1]
            content = row[2]
            self.data[sheet_name][item] = content

        return None

    def GetInfo(self, dict_name: str, key: str) -> str:
        if dict_name not in self.data:
            return ""
        if key not in self.data[dict_name]:
            return ""

        return self.data[dict_name][key]

    def _check_sheet_name(self, sheet_name) -> bool:
        self.sheet_list = self._fetch_sheet_list(
            os.path.join(self._work_dir, self._zero_file_name))

        return sheet_name in self.sheet_list

    def LoadSheets(self) -> Exception:
        self.sheet_list = self._fetch_sheet_list(
            os.path.join(self._work_dir, self._zero_file_name))
        return None

    def _fetch_sheet_list(self, fileName: str) -> list:
        """获取excel文件sheet列表

        Args:
            fileName (str): _description_

        Returns:
            list: _description_
        """
        wb = openpyxl.load_workbook(fileName)
        sheet_list = wb.get_sheet_names()
        return sheet_list
