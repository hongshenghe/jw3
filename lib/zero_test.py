# -*- encoding: utf-8 -*-
'''
@File    :   dict_test.py
@Time    :   2023/01/07 20:29:45
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   None
'''

# 字典测试

import os
import unittest
from pathlib import Path

from lib.zero import JWZero

work_dir = Path(__file__).resolve().parent.parent


class TestZero(unittest.TestCase):
    jwZero = None

    def setUp(self) -> None:
        self.jwZero = JWZero(work_dir,
                             os.path.join("upload", "00-天翼云集成实施基本信息表模板(网络和服务器设备表含公式)20230101(1).xlsx"))

        return super().setUp()

    def test_get_project_name(self):
        err = self.jwZero.LoadProject()
        project_name = self.jwZero.GetProject("项目名称")
        self.assertIsNotNone(project_name)
        print("项目名称:%s" % project_name)

    def test_get_project_id(self):
        err = self.jwZero.LoadProject()
        project_id = self.jwZero.GetProject("项目编号")
        self.assertIsNotNone(project_id)
        print("项目编号:%s" % project_id)

    def test_load_data(self):
        err = self.jwZero.LoadData()
        self.assertFalse(err)
        self.jwZero.ShowZeroData()


if __name__ == '__main__':
    unittest.main()
