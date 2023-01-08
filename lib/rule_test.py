# -*- encoding: utf-8 -*-
'''
@File    :   rule_test.py
@Time    :   2023/01/08 09:33:19
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   None
'''

# 配置规则测试用例
from lib.zero import JWZero
from lib.rule import LoadRules, JWRule
from lib.base import ensurePath, generate_batchid

import os
import unittest
from pathlib import Path


work_dir = Path(__file__).resolve().parent.parent


class TestRule(unittest.TestCase):
    jwZero = None
    jwRules = None

    def setUp(self) -> None:
        self.jwZero = JWZero(work_dir,
                             os.path.join("upload", "00-天翼云集成实施基本信息表模板(网络和服务器设备表含公式)20230101(1).xlsx"))

        self.jwRules = LoadRules(work_dir, self.jwZero)

        return super().setUp()

    def test_load_rules(self):
        self.assertGreater(len(self.jwRules), 0)

    def test_rule_generate(self):
        batch_id = generate_batchid()

        rule = JWRule(batch_id, work_dir, "05.yaml", self.jwZero)
        err = rule.Generate()
        self.assertIsNone(err)
