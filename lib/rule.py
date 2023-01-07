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
from lib.zero import JWZero
from lib.base import ensurePath


class Rule(object):
    file_name = ""
    work_dir = ""
    batch_id = ""

    def __init__(self,batch_id:str,work_dir:str,file_name:str) -> None:
        fn = os.path.join(work_dir,"rules",file_name)
        if not os.path.exists(fn):
            return
        self.file_name = file_name
        self.work_dir = work_dir
        self.batch_id = batch_id

    def Generate(self,zero:JWZero) ->Exception:
        ensurePath(os.path.join(self.work_dir,"down",self.batch_id))
        return None



# 加载所有规则
def LoadRules(work_dir: str) -> list(Rule):
    if not os.path.exists(os.path.join(work_dir,"rules")):
        return []
    
    return []
