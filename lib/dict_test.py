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

from lib.dict import JWDict

work_dir = Path(__file__).resolve().parent.parent


class TestLoadSheetName(unittest.TestCase):
    jwDict = None

    def setUp(self) -> None:
        self.jwDict = JWDict(work_dir,
                             os.path.join("docs", "00-天翼云集成实施基本信息表模板(网络和服务器设备表含公式)20230101(1).xlsx"))

        print(self.jwDict.sheet_list)

        return super().setUp()

    def test_get_sheets(self):
        err = self.jwDict.LoadSheets()
        self.assertFalse(err)

    def test_load_projects(self):
        err = self.jwDict.LoadProject()
        self.assertFalse(err)

    def test_get_project_name(self):
        err = self.jwDict.LoadProject()
        project_name = self.jwDict.GetInfo("项目信息", "项目名称")
        self.assertIsNotNone(project_name)
        print("项目名称:%s" % project_name)

    def test_get_project_id(self):
        err = self.jwDict.LoadProject()
        project_id = self.jwDict.GetInfo("项目信息", "项目编号")
        self.assertIsNotNone(project_id)
        print("项目编号:%s" % project_id)


if __name__ == '__main__':
    unittest.main()
