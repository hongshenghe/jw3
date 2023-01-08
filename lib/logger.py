# -*- encoding: utf-8 -*-
'''
@File    :   logger.py
@Time    :   2023/01/07 18:25:57
@Author  :   Hongsheng He
@Version :   1.0
@Contact :   24836227@qq.com
@License :   (C)Copyright 2007-2023, hongsheng
@Desc    :   创建日志记录器
'''


from logging.handlers import RotatingFileHandler
import logging
logger = logging.getLogger()

# 设置日志级别
logger.setLevel(logging.DEBUG)

# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler(
    "jw.log", maxBytes=1024 * 1024 * 100, backupCount=10)
stream_handler = logging.StreamHandler()  # 往屏幕上输出

# 创建日志记录的格式
formatter = logging.Formatter(
    '%(levelname)s %(asctime)s %(filename)s:第%(lineno)d行: %(message)s')

# 设置日志记录格式
file_log_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# 添加日志记录器
logging.getLogger().addHandler(file_log_handler)
logging.getLogger().addHandler(stream_handler)

# 使用方式
# logging.debug("这条日志是debug级别")
# logging.info("这条日志是info级别")
# logging.warning("这条日志是warning级别")
# logging.error("这条日志是error级别")
# logging.critical("这条日志是critical级别")
