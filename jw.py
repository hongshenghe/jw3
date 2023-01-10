# -*- encoding: utf-8 -*-
'''
@File    :   jw.py
@Time    :   2023/01/07 13:39:48
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   None
'''

# 交维数据
from pathlib import Path
import sys

from lib.jiaowei import JiaoWei
from lib.logger import logging

BASE_DIR = Path(__file__).resolve().parent


def main():
    jw = JiaoWei(
        BASE_DIR, "00-天翼云集成实施基本信息表模板(网络和服务器设备表含公式)20230101(1).xlsx", 'dict.xlsx')
    jw.Run()


if __name__ == "__main__":
    main()
