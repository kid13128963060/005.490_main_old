# -*- coding: utf-8 -*-
# version: V1.1
import subprocess
import sys
import time
import os

# 一级根目录：App总根目录
app_root = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App"
# 新增二级根路径：module文件夹专用根路径
module_root = os.path.join(app_root, "module")

# module目录脚本，改用二级module_root拼接
path2_py = os.path.join(module_root, "read_excel_once.py")

#EXCEL_PATH = r"E:\自动同步_只增加\设备识别\设备识别.xls"

# 从命令行参数获取变量6 action_code；没有传入则默认1
if len(sys.argv) >= 2:
    action_code = int(sys.argv[1])
else:
    action_code = 1

def run_python_script(script_path, capture_output_flag=False):
    # 封装执行python脚本的函数
    # capture_output_flag=True时捕获标准输出，用于获取脚本输出字符串
    if capture_output_flag:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )
    else:
        # 不捕获输出时，依然返回CompletedProcess，不再返回None
        result = subprocess.run(["python", script_path])
    return result




def close_wifi(net_adapter_name):
    """关闭wifi，入参：变量1(网卡名称)"""
    cmd = [
        "powershell",
        "-Command",
        f'Disable-NetAdapter -Name "{net_adapter_name}" -Confirm:$false'
    ]
    subprocess.run(cmd, shell=True)


def open_wifi(net_adapter_name):
    """打开wifi，入参：变量1(网卡名称)"""
    cmd = [
        "powershell",
        "-Command",
        f'Enable-NetAdapter -Name "{net_adapter_name}" -Confirm:$false'
    ]
    subprocess.run(cmd, shell=True)

def open_or_close_wifi():
    # 开启输出捕获，拿到Excel行2列2的值
    proc_result = run_python_script(path2_py, capture_output_flag=True)
    simulator_str = proc_result.stdout.strip()
    cell_value = simulator_str
    
    # 文件4内部不再from导入device_recognize，本脚本独立运行
    

    print(f"\n读取Excel行2列2的值：{cell_value}")
    if cell_value == "家脑模拟器":
        current_device = 1
    elif cell_value == "工脑模拟器":
        current_device = 2
    else:
        print("无法识别设备，不执行wifi操作")
        return

    print("========== 设备识别工作流开始 ==========")
    print(f"【current_device】= {current_device}")

    wifi_name = None
    if current_device == 1:
        wifi_name = "WLAN 2"
    elif current_device == 2:
        wifi_name = "WLAN"
    else:
        print("无法识别设备，不执行wifi操作")
        return

    action_str = None
    if action_code == 1:
        action_str = "Open"
    elif action_code == 2:
        action_str = "Close"

    print(
        f"变量1(wifi_name)={wifi_name}，变量2(action_str)={action_str}，变量6(action_code)={action_code}")

    if action_str == "Open":
        open_wifi(wifi_name)
    elif action_str == "Close":
        close_wifi(wifi_name)

if __name__ == "__main__":
    open_or_close_wifi()
