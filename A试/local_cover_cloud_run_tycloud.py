# -*- coding: utf-8 -*-
# version: V1.0.16
# 功能:调用路径1ps1脚本、path2_py、path3_py、path4_py；先执行ps1，
#       延时后依次执行py脚本；捕获path2_py读取Excel得到模拟器标识字符串，
#       根据不同模拟器标识执行不同等待时长，最后执行wifi开关脚本
# 修改说明：V1.0.15 删除本文件内部旧run_python_script实现，
#       导入module.run_python_script新版本函数；调用改为传入脚本短名，
#       由函数内部find_target_script自动搜索完整路径，自动区分py/ps1执行
# 修改说明：V1.0.16 提前初始化CELL_READ_CONST变量，修复Pylance未绑定变量警告
import os
import subprocess
import time

# ==========顶部配置区（放在一级根目录app_root上方）==========
# module脚本名字典，集中维护module目录全部脚本文件名，key从0顺序递增
module_script_dict = {
    0: "read_excel_once.py",
    1: "open_plus_close_wifi.py",
    2: "check_network_request_True.py",
}
# =========================================================

# 一级根目录：App总根目录
app_root = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App"
# 新增二级根路径：module文件夹专用根路径
module_root = os.path.join(app_root, "module")
Combination_Module_root = os.path.join(app_root, "Combination_Module")

# ps1脚本，使用一级app_root拼接，不在module搜索范围内，保留原有pwsh调用
path1_ps1 = os.path.join(app_root, "云端_本地配置_互传", "本地覆盖云端配置.ps1")

# start_tycloud脚本，使用一级app_root拼接
path3_py = os.path.join(app_root, "start_tycloud", "start_tycloud.py")
FILE6_TyCloud_SyncCheck = os.path.join(Combination_Module_root, "TyCloud_UIA_SyncStatusCheck.py")  # 文件6

# --------------------------
# 根据字典自动生成module脚本完整路径列表，key和列表下标严格一一对应
# 后续字典增加key，此列表自动变长，不需要手动新增path变量
module_path_list = []
sorted_keys = sorted(module_script_dict.keys())
for k in sorted_keys:
    full_path = os.path.join(module_root, module_script_dict[k])
    module_path_list.append(full_path)
# --------------------------

# 索引映射（和字典key保持一致）
# module_path_list[0] → read_excel_once.py
# module_path_list[1] → open_plus_close_wifi.py
# module_path_list[2] → check_network_request_True.py

# 【重要】导入外部新版执行函数，移除本文件旧版run_python_script定义
from module.run_python_script import run_python_script

# 本地覆盖云端配置，ps1脚本保留原有pwsh调用方式
subprocess.run(["pwsh", "-ExecutionPolicy", "Bypass", "-File", path1_ps1], check=False)

time.sleep(5)  # 等待5秒，确保ps1脚本执行完成

# ======================修复点：预先初始化变量======================
CELL_READ_CONST = ""
# 获取模拟器标识 对应脚本短名 read_excel_once
ret_read_excel = run_python_script("read_excel_once", capture_output_flag=True)
# 做None防护，防止脚本未找到报错
if ret_read_excel is None:
    print("错误：未找到 read_excel_once 脚本，程序终止")
else:
    CELL_READ_CONST = ret_read_excel.stdout.strip()
    print(CELL_READ_CONST)

# check_network_request_True.py 对应短名 check_network_request_True
ret_net = run_python_script("check_network_request_True", capture_output_flag=True)
if ret_net is None:
    print("错误：未找到 check_network_request_True 脚本")
    net_ok = ""
else:
    net_ok = ret_net.stdout.strip()

print(f"net_ok：{net_ok}")


# 没网打开Wifi
if not net_ok:
    print("检测结果：无网络(net_ok=False)，执行文件4 open_plus_close_wifi")
    run_python_script("open_plus_close_wifi")
else:
    print("检测结果：网络正常，跳过执行文件4 open_plus_close_wifi")

# start_tycloud，脚本短名 start_tycloud
run_python_script("start_tycloud")

# CELL_READ_CONST现在一定存在，消除Pylance警告
if CELL_READ_CONST == "家脑模拟器":
    print("家脑模拟器标识字符串匹配成功")
    time.sleep(5)
elif CELL_READ_CONST == "工脑模拟器":
    print("工脑模拟器标识字符串匹配成功")
    time.sleep(15)
else:
    print("模拟器标识字符串不匹配")

# TyCloud_UIA_SyncStatusCheck，脚本短名 TyCloud_UIA_SyncStatusCheck
run_python_script("TyCloud_UIA_SyncStatusCheck")

# 再次执行wifi开关脚本 open_plus_close_wifi
run_python_script("open_plus_close_wifi")
