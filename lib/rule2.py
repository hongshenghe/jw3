# -*- encoding: utf-8 -*-
'''
@File    :   rule.py
@Time    :   2023/01/07 18:04:41
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   None
'''

# 规则文件

import os
import yaml


class Rule(object):
    """
    规则
    """
    file_id = ""
    file_name = ""
    name = ""
    meta = []
    rules = []
    content = ""
    base_dir = ""

    def __init__(self, baseDir: str, fileName: str):
        """
        初始化规则。 
        """
        fn = "%s.yaml" % fileName
        self.file_name = os.path.join(baseDir, "rules", fn)
        self.name = fileName
        self.file_id = fileName
        self.base_dir = baseDir
        self.load()

    def load(self):
        """
        加载规则文件 
        """
        if not os.path.exists(self.file_name):
            print(f"Error,File not exists,{self.file_name}")
            return

        content = ''
        with open(self.file_name, 'r', encoding="utf-8") as f:
            content = yaml.full_load(f)

        self.content = content
        self.rules = self.content['rules']
        self.meta = self.content['meta']
        self.name = self.content['meta']['name']

    def GenerateData(self):
        """
        生成数据文件。 
        """
        pass
