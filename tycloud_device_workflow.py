# -*- coding: utf-8 -*-
# version: V6.1
# 更新记录
# V1.0 基础业务实现
# V1.1 调换步骤1步骤2顺序，添加版本注释
# V1.2 FILE4改为文档给定完整绝对路径
# V1.3 步骤后增加sleep延时
# V1.4 subprocess调用文件2
# V1.5‑V3.3 替换方式1，修复gbk编码
# V6.0 全部使用替换方式2，删除所有from xxx import xxx；wrapper逻辑写在各脚本末尾；run_script严格文档签名；区分捕获输出/继承控制台规避gbk；sleep=5；net_ok=False调用文件4传入action_code=1
# V6.1 修改文件2、文件3、文件4统一路径为E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\tycloud

import os
import sys
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# =================【docx指定统一文件夹路径】================
BASE_TYCLOUD_OLD = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\tycloud"
FILE2_DEV_RECOG = os.path.join(BASE_TYCLOUD_OLD, "device_recognize.py")      # 文件2
FILE3_NET = os.path.join(BASE_TYCLOUD_OLD, "check_network_request.py")        # 文件3
FILE4_OPEN_WIFI = os.path.join(BASE_TYCLOUD_OLD, "open_plus_close_wifi.py")   # 文件4

START_TYCLOUD_PATH = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\start_tycloud\start_tycloud.py"
# ==============================================================================


# 严格文档函数签名 def run_script(path, label, extra_args=None):
def run_script(path, label, extra_args=None):
    """
    替换方式2调用外部脚本
    文件2、文件3：捕获stdout，解析标记获取返回值
    文件4、start_tycloud：stdout/stderr继承控制台，不捕获，规避gbk编码报错
    return: (returncode, stdout_text)
    """
    if extra_args is None:
        extra_args = []
    print(f"\n---- 执行{label}  {path} {extra_args} ----")
    if not os.path.exists(path):
        print(f"错误：文件不存在 {path}")
        return -1, ""
    cmd_list = [sys.executable, path] + extra_args
    filename = os.path.basename(path)
    if filename in ("device_recognize.py","check_network_request.py"):
        result = subprocess.run(cmd_list, capture_output=True, text=True, errors="replace")
        return result.returncode, result.stdout
    else:
        # open_plus_close_wifi.py / start_tycloud.py 业务脚本直接输出控制台
        result = subprocess.run(cmd_list, stdout=None, stderr=None)
        return result.returncode, ""


def main():
    print("========== 设备识别工作流开始 ==========")

    #【步骤1】替换方式2：子进程调用文件2 device_recognize.py，解析DEV_RET标记，获取current_device
    ret_code, out_dev = run_script(FILE2_DEV_RECOG, "调用文件2 device_recognize")
    current_device = None
    for line in out_dev.splitlines():
        if line.startswith("DEV_RET:"):
            val = line.split(":",1)[1].strip()
            if val == "1":
                current_device = 1
            elif val == "2":
                current_device = 2
            else:
                current_device = None
    print(f"【current_device】= {current_device}")

    #【步骤2（步骤2+3合并）】替换方式2：子进程调用文件3 check_network_request.py，解析NET_RET标记获取net_ok
    ret_code, out_net = run_script(FILE3_NET, "调用文件3 check_network_request")
    net_ok = False
    for line in out_net.splitlines():
        if line.startswith("NET_RET:"):
            val = line.split(":",1)[1].strip()
            net_ok = (val == "True")
    print(f"【net_ok】={net_ok}")

    # 文档要求：变量5 net_ok=False，则文件4变量6 action_code=1
    if not net_ok:
        print("检测结果：无网络(net_ok=False)，执行文件4 open_plus_close_wifi，传入action_code=1")
        run_script(FILE4_OPEN_WIFI, "文件4 open_plus_close_wifi.py", extra_args=["1"])
    else:
        print("检测结果：网络正常，跳过执行文件4 open_plus_close_wifi")

    print("\n合并步骤执行完成，延时等待5秒……")
    time.sleep(5)

    print("\n>>>> 等待结束，执行路径1：start_tycloud.py天翼云盘脚本")
    run_script(START_TYCLOUD_PATH, "start_tycloud.py")

    print("\n========== 设备识别工作流全部执行结束 ==========")


if __name__ == "__main__":
    main()
