# -*- encoding: utf-8 -*-
'''
@File    :   rule.py
@Time    :   2023/01/07 22:05:27
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   规则管理
'''


import os

import openpyxl
import pandas as pd
import yaml
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, PatternFill, Side

from lib.base import ensurePath, generate_batchid
from lib.logger import logging
from lib.utils._05 import (GenerateProjectSiteInfo, GetProjectDict, SetNone,
                           SetValue, GetProjectSite,GetRackProductLine)
from lib.utils._09 import Copy, GetDict
from lib.zero import JWZero
from lib.dict import JWDict


class JWRule(object):

    zero = None
    jwDict = None

    # 文件编号
    file_id = ""

    # 文件名称
    file_name = ""
    work_dir = ""
    batch_id = ""

    # 配置文件原始内容
    content = ""
    # 配置文件名称
    name = ""
    # 配置文件meta信息
    meta = []
    # 配置文件规则
    rules = []

    error = None

    def __init__(self, batch_id: str, work_dir: str, file_id: str, zero: JWZero, jwDict: JWDict) -> None:

        self.file_name = "%s.yaml" % file_id
        full_name = os.path.join(work_dir, "rules",  self.file_name)

        logging.info("file_id: %s" % file_id)
        logging.info("full_name: %s" % full_name)

        if not os.path.exists(full_name):
            return

        self.file_id = file_id
        self.work_dir = work_dir
        self.batch_id = batch_id
        self.zero = zero
        self.jwDict = jwDict

    def Generate(self) -> Exception:
        # 生成路径
        output_dir = os.path.join(self.work_dir, "down", self.batch_id)
        ensurePath(output_dir)

        # load
        err = self.load()
        if err:
            return err

        # generate data
        # 动态数据计算
        file_name = self.generate_output_file_name()
        output = os.path.join(output_dir, '%s.xlsx' % file_name)
        data = {}
        for sheet in self.rules:

            sheet_name = sheet['sheet_name']
            sheet_type = "动态计算" if "sheet_type" not in sheet else sheet['sheet_type']
            order = None if "order" not in sheet else sheet['order']
            content = None if "content" not in sheet else sheet['content']

            if sheet_type == "fixed":
                continue

            logging.info("处理 %s-%s 开始" % (self.file_id, sheet_name))
            logging.info("  sheet类型: %s" % (sheet_type))

            df = pd.DataFrame()
            col_id = 1
            for r in sheet['columns']:
                col_name = r['name']
                value = None if "value" not in r else r['value']
                source_sheet = None if "source_sheet" not in r else r['source_sheet']
                source_column = None if "source_column" not in r else r['source_column']

                logging.info("处理 %s-%s，第%s列,%s" %
                             (self.file_id, sheet_name, col_id, col_name))
                df, flag = eval(r['method'])(
                    self.zero, self.jwDict, df, col_name, value, source_sheet, source_column)

                col_id += 1
            data[sheet_name] = df
            logging.info("处理 %s-%s 结束" % (self.file_id, sheet_name))

        self._save_excel(output, data)

        # 固定表格生成
        for sheet in self.rules:
            sheet_name = sheet['sheet_name']
            sheet_type = "动态计算" if "sheet_type" not in sheet else sheet['sheet_type']
            order = None if "order" not in sheet else sheet['order']
            # width = 50 if "width" not in sheet else sheet['width']
            content = None if "content" not in sheet else sheet['content']

            logging.info("处理 %s-%s 开始" % (self.file_id, sheet_name))
            logging.info("  sheet类型: %s" % (sheet_type))
            logging.info("  位置: %s" % (order))

            if sheet_type == "fixed":
                self._save_fixed_sheet(
                    output, sheet_name, order, content)
            logging.info("处理 %s-%s 结束" % (self.file_id, sheet_name))

        return None

    def _save_fixed_sheet(self, output_file, sheet_name, order,   content):

        if not os.path.exists(output_file):
            logging.error("%s 文件不存在，不能增加新sheet" % output_file)
            return

        wb = openpyxl.load_workbook(output_file)
        if order == "first":
            ws = wb.create_sheet(title=sheet_name, index=0)
        else:
            ws = wb.create_sheet(title=sheet_name)
        # ws.sheet_properties.tabColor = 'ff72BA'

        border = Border(left=Side(border_style='thin', color='000000'),
                        right=Side(border_style='thin', color='000000'),
                        top=Side(border_style='thin', color='000000'),
                        bottom=Side(border_style='thin', color='000000'))
        row_num = 1
        for c in content:
            col_num = 1
            for value in c.split("|"):
                cell = ws.cell(column=col_num, row=row_num)
                cell.value = "\n".join(value.split(" "))

                cell.border = border
                cell.alignment = Alignment(wrapText=True)

                col_num += 1

            row_num += 1
        ws.column_dimensions["A"].width = 50
        ws.column_dimensions["B"].width = 50
        # ws.column_dimensions["A"].column_width = None
        # ws.column_dimensions["B"].column_width = None
        ws.column_dimensions["A"].auto_size = True
        ws.column_dimensions["B"].auto_size = True
        ws.column_dimensions["A"].bestFit = True
        ws.column_dimensions["B"].bestFit = True
        wb.save(output_file)

    def _save_excel(self, file_name: str, data: dict) -> None:
        """保存文件"""

        writer = pd.ExcelWriter(file_name)
        for k, v in data.items():
            sheet_name = k
            df = v

            df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.close()

    def load(self) -> Exception:
        # 加载配置文件
        fn = os.path.join(self.work_dir, "rules", self.file_name)
        # print("fn:", fn)
        if not os.path.exists(fn):
            err = Exception("配置文件不存在:%s" % fn)
            self.error = err
            return err

        # logging.info("fn:",fn)
        content = ''
        with open(fn, 'r', encoding="utf-8") as f:
            content = yaml.full_load(f)

        self.content = content
        self.rules = self.content['rules']
        self.meta = self.content['meta']
        self.name = self.content['meta']['name']

        return None

    def generate_output_file_name(self) -> str:
        file_no = self.file_id.zfill(2)
        project_name = self.zero.GetProject("项目名称")
        return "%s%s--%s" % (file_no,
                             project_name, self.name)


# 加载所有规则
def LoadRules(work_dir: str, zero: JWZero, jwDict: JWDict) -> list:
    logging.info("加载所有规则文件")
    rules = []

    rule_dir = os.path.join(work_dir, "rules")
    if not os.path.exists(rule_dir):
        return rules

    batch_id = generate_batchid()

    rule_file_list = [f for f in os.listdir(
        rule_dir) if os.path.splitext(f)[1] == ".yaml"]

    rule_file_id_list = []
    for f in rule_file_list:
        file_id = str(os.path.splitext(f)[0])
        rule_file_id_list.append(file_id)

    for file_id in rule_file_id_list:
        logging.info("加载:%s.yaml" % file_id)
        rules.append(JWRule(batch_id, work_dir, file_id, zero, jwDict))

    return rules
