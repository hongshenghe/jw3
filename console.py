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
from lib.dict import JWDict

work_dir = os.getcwd()
work_dir = Path(__file__).resolve().parent

# zero 测试
zero = JWZero(work_dir,
              os.path.join("upload", "00-天翼云集成实施基本信息表模板(网络和服务器设备表含公式)20230101(1).xlsx"))
# # jwRules = LoadRules(work_dir, zero)

# batch_id = generate_batchid()
# rule = JWRule(batch_id, work_dir, "05", zero)

# err = rule.Generate()
# if err:
#     print("error:", err)


# dict 测试
jwDict = JWDict(work_dir,
                os.path.join("upload", "dict.xlsx"))



# 测试获取生成产品线
# network = zero.GetData("网络设备")[['对应设备清单-配对列', '机架', '机房']]
# server = zero.GetData("服务器")[['对应设备清单-配对列', '机架', '机房']]
# dfSummary = pd.concat([network, server], axis=0).sort_values(
#     by=['对应设备清单-配对列', '机架', '机房'], ascending=True)
# asserts = zero.GetData("设备清单")

# 测试vm规划


# server_data = zero.GetData("服务器")
# assets = zero.GetData("设备清单")
# server_data =server_data[server_data["角色"] == "KVM"][['角色','设备标签']]
# print(server_data)


# group=assets[['品牌','云调库中对应型号']].value_counts(ascending=True).reset_index()