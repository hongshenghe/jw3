# -*- encoding: utf-8 -*-
'''
@File    :   rule.py
@Time    :   2023/01/07 22:05:27
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   None
'''

# 规则

import os

import pandas as pd
import yaml

from lib.base import ensurePath, generate_batchid
from lib.logger import logging
from lib.zero import JWZero
from lib.utils._05 import GenerateProjectSiteInfo, GetProjectDict


class JWRule(object):

    zero = None

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

    def __init__(self, batch_id: str, work_dir: str, file_id: str, zero: JWZero) -> None:

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

    def Generate(self) -> Exception:
        # 生成路径
        output_dir = os.path.join(self.work_dir, "down", self.batch_id)
        ensurePath(output_dir)

        # load
        err = self.load()
        if err:
            return err

        # generate data
        data = {}
        for sheet in self.rules:
            df = pd.DataFrame()
            col_id = 1
            sheet_name = sheet['sheet_name']
            for r in sheet['columns']:
                # catalog = None if "catalog" not in r else r['catalog']
                # entry = None if "entry" not in r else r['entry']
                # source_sheet = None if "source_sheet" not in r else r['source_sheet']
                # source_column = None if "source_column" not in r else r['source_column']
                col_name = r['name']
                value = None if "value" not in r else r['value']

                logging.info("处理%s，第%s列,%s" % (sheet_name, col_id, col_name))
                df, flag = eval(r['method'])(self.zero, df, col_name, value)

                col_id += 1
            data[sheet_name] = df

        # save data
        file_name = self.generate_output_file_name()
        output = os.path.join(output_dir, '%s.xlsx' % file_name)
        self._save_excel(output, data)

        # print("output:%s" % output)

        return None

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
        if not os.path.exists(fn):
            err = Exception("配置文件不存在:%s" % fn)
            self.error = err
            return err

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
def LoadRules(work_dir: str, zero: JWZero) -> list:
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
        rules.append(JWRule(batch_id, work_dir, file_id, zero))

    return rules
