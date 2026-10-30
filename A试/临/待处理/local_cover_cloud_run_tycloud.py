# 版本: V1.1.18 Ok| 功能:调用ps1脚本、多个py脚本；先执行ps1，延时后依次执行py脚本；
#       捕获read_excel_once读取Excel得到模拟器标识字符串，根据不同模拟器标识
#       执行不同等待时长，最后执行wifi开关脚本，执行完毕关机。
# 变更记录：V1.0.16 提前初始化CELL_READ_CONST变量，修复Pylance未绑定变量警告
# 变更记录：V1.0.17 ps1脚本改用run_python_script函数调用；移除全部硬编码脚本路径；
#       删除未使用字典与路径生成逻辑；所有脚本调用增加None查找失败防护
import os
import subprocess
import time
import sys
from pathlib import Path

# 【重要】导入外部新版执行函数
from Combination_Module.run_python_script import run_python_script, run_script_get_stdout

# 一级根目录：App总根目录
app_root = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App"
Combination_Module_root = os.path.join(app_root, "Combination_Module")

# 清除Ditto剪贴板历史中未使用的剪贴项，执行Ditto_AutoDeleteUnusedClipItems.py
run_python_script("Ditto_AutoDeleteUnusedClipItems")
time.sleep(2)
# 使用run_python_script执行ps1脚本，传入不带后缀脚本短名
ret_ps1 = run_python_script("本地覆盖云端配置")
if ret_ps1 is None:
    print("错误：未找到【本地覆盖云端配置.ps1】脚本，继续往下执行")

time.sleep(3)  # 等待3秒，确保ps1脚本执行完成

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

# 步骤2：调用 check_network_request 网络检测
out = run_script_get_stdout("check_network_request")
net_ok = out == "True"
print(net_ok)

# 没网打开Wifi
if not net_ok:
    print("检测结果：无网络(net_ok=False)，执行文件4 open_plus_close_wifi")
    ret_wifi1 = run_python_script("open_plus_close_wifi", extra_args=["1"])
    if ret_wifi1 is None:
        print("警告：未找到 open_plus_close_wifi 脚本，wifi开关跳过")
else:
    print("检测结果：网络正常，跳过执行文件4 open_plus_close_wifi")


# start_tycloud，脚本短名 start_tycloud
ret_start_ty = run_python_script("start_tycloud")
if ret_start_ty is None:
    print("警告：未找到 start_tycloud 脚本")

time.sleep(10)

p = Path(r"E:\备份盘\8000_大文件夹\009_备份文件夹_自\同步用\启动云端覆盖本地用.txt")
p.parent.mkdir(parents=True, exist_ok=True)  # 建父目录，等价 -Force
p.touch(exist_ok=True)  # touch 新建空文件，exist_ok=True 已存在不报错

# TyCloud_UIA_SyncStatusCheck，脚本短名 TyCloud_UIA_SyncStatusCheck
ret_sync_check = run_python_script("TyCloud_UIA_SyncStatusCheck")
if ret_sync_check is None:
    print("警告：未找到 TyCloud_UIA_SyncStatusCheck 脚本")

# CELL_READ_CONST现在一定存在，消除Pylance警告
if CELL_READ_CONST == "家脑模拟器":
    print("家脑模拟器标识字符串匹配成功")
    time.sleep(5)
elif CELL_READ_CONST == "工脑模拟器":
    print("工脑模拟器标识字符串匹配成功")
    run_python_script("open_plus_close_wifi", extra_args=["2"])
    time.sleep(7)
    p.unlink(missing_ok=True)  # missing_ok=True：文件不存在不抛异常，类似 -Force

    # 测试阶段建议注释，避免直接关机
    subprocess.run(["shutdown", "/s", "/t", "40"], check=True)
else:
    print("模拟器标识字符串不匹配")
