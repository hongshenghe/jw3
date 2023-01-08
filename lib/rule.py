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
from lib.logger import logging
from lib.zero import JWZero
from lib.base import ensurePath, generate_batchid


class JWRule(object):
    file_id = ""
    file_name = ""
    work_dir = ""
    batch_id = ""

    def __init__(self, batch_id: str, work_dir: str, file_name: str, zero: JWZero) -> None:
        fn = os.path.join(work_dir, "rules", file_name)
        if not os.path.exists(fn):
            return
        self.file_name = file_name
        self.work_dir = work_dir
        self.batch_id = batch_id

    def Generate(self) -> Exception:
        # 生成路径
        ensurePath(os.path.join(self.work_dir, "down", self.batch_id))

        return None


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
        # print("file_id:%s\n" % file_id)
        logging.info("加载:%s.yaml" % file_id)

        rules.append(JWRule(batch_id, work_dir, "%s.yaml" % file_id, zero))
    return rules
