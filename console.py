# -*- encoding: utf-8 -*-
'''
@File    :   console.py
@Time    :   2023/01/08 11:24:02
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2020, hongsheng
@Desc    :   单体测试
'''
import os
import shutil
from pathlib import Path

import pandas as pd

from lib.base import ensurePath, generate_batchid
from lib.rule import JWRule, LoadRules
from lib.zero import JWZero

work_dir = Path(__file__).resolve().parent

zero = JWZero(work_dir,
              os.path.join("upload", "00-天翼云集成实施基本信息表模板(网络和服务器设备表含公式)20230101(1).xlsx"))
# jwRules = LoadRules(work_dir, zero)

batch_id = generate_batchid()
rule = JWRule(batch_id, work_dir, "05", zero)

err = rule.Generate()
if err:
    print("error:", err)


 
