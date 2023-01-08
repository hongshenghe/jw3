# -*- encoding: utf-8 -*-
'''
@File    :   jiaowei.py
@Time    :   2023/01/07 18:01:52
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   None
'''

import os
import sys

from lib.logger import logging
from lib.dict import JWDict
from lib.base import ensurePath


class JiaoWei:
    work_dir = ""
    zero_file = ""
    jwDict = None

    def __init__(self, work_dir: str, zero_file: str) -> None:

        logging.info("work_dir:%s" % work_dir)
        logging.info("zero_file:%s" % zero_file)

        self.work_dir = work_dir
        self.ensureDirectory()
        self.zero_file = os.path.join(work_dir, "upload", zero_file)

    def ensureDirectory(self):
        ensurePath(os.path.join(self.work_dir, "down"))

    def LoadZero(self) -> Exception:
        if not os.path.exists(self.zero_file):
            return Exception("Error:零号文件不存在,%s" % self.zero_file)

        self.jwDict = JWDict(self.work_dir, self.zero_file)
        return None

    def Run(self):
        logging.info("开始生成交维数据")

        err = self.LoadZero()
        if err:
            logging.error("加载零号文件失败,%s" % err)
            sys.exit(1)

        # err = self.LoadDict()
        # if err:
        #     logging.error("加载字典失败,%s" % err)
        #     sys.exit(1)

        logging.info("生成交维数据结束")
