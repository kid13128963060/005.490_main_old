# -*- coding: utf-8 -*-
# version: V1.0
import subprocess
import sys

EXCEL_PATH = r"E:\自动同步_只增加\设备识别\设备识别.xls"

# 从命令行参数获取变量6 action_code；没有传入则默认2
if len(sys.argv) >= 2:
    action_code = int(sys.argv[1])
else:
    action_code = 1


def open_or_close_wifi():
    # 文件4内部不再from导入device_recognize，本脚本独立运行
    import xlrd
    wb = xlrd.open_workbook(EXCEL_PATH)
    sheet = wb.sheet_by_index(0)
    cell_value = sheet.cell_value(rowx=1, colx=1)
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

    print(f"变量1(wifi_name)={wifi_name}，变量2(action_str)={action_str}，变量6(action_code)={action_code}")

    if action_str == "Open":
        open_wifi(wifi_name)
    elif action_str == "Close":
        close_wifi(wifi_name)


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


if __name__ == "__main__":
    open_or_close_wifi()
