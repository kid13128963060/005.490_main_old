# -*- coding: utf-8 -*-
# version: V3.3
import os
import sys
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# =========替换方式1 from xxx import xxx=========
from check_network_request import check_network_request
from device_recognize import get_current_device

# ====================常量配置（文档给定路径）====================
FILE1 = os.path.join(BASE_DIR, "open_plus_close_wifi.py")   # 文件1
FILE2 = os.path.join(BASE_DIR, "check_network_request.py")  # 文件2
# 文档路径1 start_tycloud.py完整绝对路径
FILE4 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\start_tycloud\start_tycloud.py"


def run_script(path, label, extra_args=None):
    """执行外部py脚本，【修复】不捕获stdout/stderr，子进程直接继承控制台，规避gbk编码报错"""
    if extra_args is None:
        extra_args = []
    print(f"\n---- 执行{label}  {path} {extra_args} ----")
    if not os.path.exists(path):
        print(f"错误：文件不存在 {path}")
        return -1
    cmd_list = [sys.executable, path] + extra_args
    # stdout=None、stderr=None：子进程直接输出到当前控制台，不捕获，彻底避开编码转换报错
    result = subprocess.run(cmd_list, stdout=None, stderr=None)
    return result.returncode


def main():
    print("========== 设备识别工作流开始 ==========")

    #【步骤1】读取Excel获取current_device
    current_device = get_current_device()
    print(f"【current_device】= {current_device}")

    #【步骤2（步骤2+3合并）】调用文件2网络检测函数
    print("\n---- 调用文件2 check_network_request() 网络检测 ----")
    net_ok = check_network_request(timeout=3)

    # =========文档要求3：变量5 net_ok = False，则文件1代码1中变量6 action_code =1 =========
    if not net_ok:
        print("检测结果：无网络(net_ok=False)，执行文件1，传入action_code=1")
        # extra_args 传入 ["1"] → 文件1接收sys.argv[1]=1，对应变量6 action_code=1
        run_script(FILE1, "文件1(open_plus_close_wifi.py)", extra_args=["1"])
    else:
        print("检测结果：网络正常，跳过执行文件1")

    # ----------------【衔接检查：步骤3 ↔ 文件4(start_tycloud)】----------------
    # 1.合并步骤调用from导入的文件2函数做网络判断；net_ok=False调用文件1并且传入action_code=1；
    # 2.延时15秒，等待网卡、网络环境稳定；
    # 3.FILE4(start_tycloud.py)内部自带独立socket网络检测、pid锁、最大360s等待；
    # 4.两套网络检测互相独立互不冲突；延时结束无条件运行FILE4；✅衔接无问题
    print("\n合并步骤执行完成，延时等待15秒……")
    time.sleep(5)

    print("\n>>>> 等待结束，执行路径1：文件4【start_tycloud.py】天翼云盘脚本")
    run_script(FILE4, "文件4(天翼云盘启动脚本)")

    print("\n========== 设备识别工作流全部执行结束 ==========")


if __name__ == "__main__":
    main()
