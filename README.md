# 交维


## 优先级

```bash
# 运维
√ 05.机柜导入
√ 06.VLAN表
√ 07.AS表
√ 09.交维网络设备导入表
√ 09.交维网络设备表上传表（COC）
√ 10.交维物理设备导入表
√ 10.交维物理设备表上传表（COC）
√ 12.服务器4A纳管
√ 13.网络设备4A纳管 
√ 15.普罗米修斯
√ 17.出口带宽
16.维保信息
√ 32.IP地址段

# 自动化验收
√ 49.网络自动化验收表
√ 50.服务器自动化验收表

# 云调
√ 51.采集机交维
√ 52.采集机信息收纳表

# 研二云桌面
√ 61.云桌面网络设备交维模板(研发)
√ 62.云桌面服务器交维模板(研发)

# 研三
# TODO
```


## 开发运行环境配置

1. 建立虚拟环境

```bash
python3 -m venv venv
```

2. 安装依赖包

windows
```cmd
D:\projects\python\jw3>venv\Scripts\activate
(venv) D:\projects\python\jw3>pip install -r requirements.txt
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already satisfied: pandas==1.5.2 in d:\projects\python\jw3\venv\lib\site-packages (from -r requirements.txt (line 1)) (1.5.2)
Requirement already satisfied: openpyxl==3.0.10 in d:\projects\python\jw3\venv\lib\site-packages (from -r requirements.txt (line 2)) (3.0.10)
Requirement already satisfied: PyYAML==6.0 in d:\projects\python\jw3\venv\lib\site-packages (from -r requirements.txt (line 3)) (6.0)
Requirement already satisfied: python-dateutil>=2.8.1 in d:\projects\python\jw3\venv\lib\site-packages (from pandas==1.5.2->-r requirements.txt (line 1)) (2.8.2)
Requirement already satisfied: pytz>=2020.1 in d:\projects\python\jw3\venv\lib\site-packages (from pandas==1.5.2->-r requirements.txt (line 1)) (2022.7)
Requirement already satisfied: numpy>=1.21.0 in d:\projects\python\jw3\venv\lib\site-packages (from pandas==1.5.2->-r requirements.txt (line 1)) (1.24.1)
Requirement already satisfied: et-xmlfile in d:\projects\python\jw3\venv\lib\site-packages (from openpyxl==3.0.10->-r requirements.txt (line 2)) (1.1.0)
Requirement already satisfied: six>=1.5 in d:\projects\python\jw3\venv\lib\site-packages (from python-dateutil>=2.8.1->pandas==1.5.2->-r requirements.txt (line 1)) (1.16.0)
```

3. 执行测试用例

```bash
(venv) ➜  jw3 git:(master) ✗ python -m unittest lib/rule_test.py
```

4. 程序执行
   
    4.1 双击执行sbin/run.cmd
    4.2 在down目录查找最新目录
