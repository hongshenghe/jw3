# -*- encoding: utf-8 -*-
'''
@File    :   zero.py
@Time    :   2023/01/07 22:05:27
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   零号表管理
'''

import pandas as pd
import os

from lib.base import fetchExcelSheets


class JWZero(object):
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
    # }
    data = {}

    sheet_list = []

    def __init__(self, work_dir: str, zero_file: str) -> None:
        """零号表数据初始化

        Args: 
            work_dir (str): 工作目录
            zero_file (str): 零号数据文件名称
        """
        self._work_dir = work_dir
        self._zero_file_name = zero_file
        self._load_sheet_names()
        self.LoadProject()
        self.LoadData()

    def LoadProject(self) -> Exception:
        sheet_name = "项目信息"
        if sheet_name not in self.data:
            self.data[sheet_name] = {}

        # sheet是否存在
        if not self._check_sheet_name(sheet_name):
            return Exception("Error:%s 表格不存在" % sheet_name)

        # 加载sheet
        df = pd.read_excel(os.path.join(
            self._work_dir, self._zero_file_name), sheet_name=sheet_name, engine='openpyxl')
        for i, row in df.iterrows():
            item = row[1]
            content = row[2]
            self.data[sheet_name][item] = content

        return None

    def _load_sheet_names(self) -> None:
        self.sheet_list = fetchExcelSheets(
            os.path.join(self._work_dir, self._zero_file_name))

    def _check_sheet_name(self, sheet_name) -> bool:
        return sheet_name in self.sheet_list

    def GetProject(self, key: str) -> str:
        dict_name = "项目信息"
        if dict_name not in self.data:
            return ""
        if key not in self.data[dict_name]:
            return ""

        return self.data[dict_name][key]

    def LoadData(self) -> Exception:
        for sheet_name in self.sheet_list:
            if sheet_name == "项目信息":
                continue
            err = self._loadDataFrame(sheet_name)
            if err:
                return err

    def ShowZeroData(self):
        for k, v in self.data.items():
            print("data name:%s \n data value:%s" % (k, v))

    def _loadDataFrame(self, data_name: str) -> Exception:
        if data_name not in self.data:
            self.data[data_name] = None

        # data sheet 是否存在
        if not self._check_sheet_name(data_name):
            return Exception("Error:%s 表格不存在" % data_name)

        # 加载sheet
        df = pd.read_excel(os.path.join(
            self._work_dir, self._zero_file_name), sheet_name=data_name, engine='openpyxl')

        self.data[data_name] = df
        return None

    def GetData(self, dict_name: str) -> pd.DataFrame:
        if dict_name not in self.data:
            return None

        return self.data[dict_name]
