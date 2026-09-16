# -*- coding: utf-8 -*-
# version: V1.2
# 更新记录
# V1.0 基础版本实现业务分支
# V1.1 调换步骤1步骤2顺序，添加版本注释
# V1.2 修改FILE4为文档给定完整绝对路径，核对全部需求，输出衔接检查说明

import os
import sys
import subprocess
import xlrd

# ==================== 常量配置（文档给定路径，可修改） ====================
EXCEL_PATH = r"E:\自动同步_只增加\设备识别\设备识别.xls"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE1 = os.path.join(BASE_DIR, "open_plus_close_wifi.py")   # 文件1
FILE2 = os.path.join(BASE_DIR, "check_network_request.py")  # 文件2
# 文档【路径1】完整绝对路径
FILE4 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\start_tycloud\start_tycloud.py"

sys.path.insert(0, BASE_DIR)


def run_script(path, label):
    """执行外部py脚本，打印输出与错误"""
    print(f"\n---- 执行{label}  {path} ----")
    if not os.path.exists(path):
        print(f"错误：文件不存在 {path}")
        return -1
    result = subprocess.run([sys.executable, path],
                            capture_output=True, text=True)
    print(result.stdout, end="")
    if result.stderr:
        print("stderr:", result.stderr)
    return result.returncode


def check_network():
    """网络检测：ping百度；True=有网，False=断网"""
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "2000", "www.baidu.com"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        print("网络检测异常：", e)
        return False


def get_current_device():
    """读取Excel第2行第2列：家脑模拟器=1，工脑模拟器=2，其他返回None"""
    wb = xlrd.open_workbook(EXCEL_PATH)
    sheet = wb.sheet_by_index(0)
    cell_value = sheet.cell_value(rowx=1, colx=1)
    print(f"\n读取Excel行2列2的值：{cell_value}")

    if cell_value == "家脑模拟器":
        return 1
    elif cell_value == "工脑模拟器":
        return 2
    else:
        print("未匹配模拟器类型")
        return None


def run_command1():
    """命令1：禁用WLAN 2网卡，必须管理员权限运行"""
    print("\ncurrent_device=1，执行禁用WLAN2网卡命令")
    cmd = ["powershell", "-Command",
           'Disable-NetAdapter -Name "WLAN 2" -Confirm:$false']
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("stdout：", result.stdout)
    print("stderr：", result.stderr)


def call_open_wifi():
    """调用文件1 open_plus_close_wifi.py 的 open_wifi()"""
    print("\ncurrent_device=2，调用open_plus_close_wifi.py 的 open_wifi()")
    if not os.path.exists(FILE1):
        print(f"错误：{FILE1} 文件找不到！")
        return
    import open_plus_close_wifi
    if hasattr(open_plus_close_wifi, "open_wifi"):
        open_plus_close_wifi.open_wifi()
    else:
        print("警告：文件1内没有找到 open_wifi 函数")


def main():
    print("========== 设备识别工作流开始 ==========")

    # 【调换后步骤1】读取Excel获取current_device（原步骤2移至此处）
    current_device = get_current_device()
    print(f"【current_device】= {current_device}")

    # 【调换后步骤2】执行文件2 check_network_request.py（原步骤1移至此处）
    run_script(FILE2, "文件2(check_network_request.py)")

    # 【步骤3】网络判断：没网执行文件1；有网跳过文件1
    net_ok = check_network()
    if not net_ok:
        print("检测结果：无网络，执行文件1(open_plus_close_wifi.py)")
        run_script(FILE1, "文件1(open_plus_close_wifi.py)")
    else:
        print("检测结果：网络正常，跳过执行文件1")

    # ----------------步骤3与步骤4衔接检查----------------
    # 说明：
    # 1.步骤3的ping网络检测仅用于控制是否运行文件1；
    # 2.文件4 start_tycloud.py内部使用socket独立网络检测，自带最多360秒等待，单实例pid锁；
    # 3.无论步骤3网络结果如何，都无条件调用文件4；文件4内部自行处理网络等待、超时退出；
    # ✔衔接无问题，两套网络检测逻辑互不干扰。
    print("\n>>>> 步骤3执行完毕，进入步骤4，准备执行文件4【start_tycloud.py】天翼云盘脚本")
    import time
    print("步骤3结束，等待15秒后再运行文件4……")
    time.sleep(15)
    run_script(FILE4, "文件4(天翼云盘启动脚本)")

    # 业务分支逻辑
    if current_device == 1:
        run_command1()
    elif current_device == 2:
        call_open_wifi()
    else:
        print("current_device为空，不执行设备对应操作")

    print("\n========== 设备识别工作流结束 ==========")


if __name__ == "__main__":
    main()
