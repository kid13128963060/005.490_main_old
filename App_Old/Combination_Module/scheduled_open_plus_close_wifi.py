# Version: V6.4 | Function:基于代码1原版框架获取系统时间判断时间区间，
#           生成字符串类型extra_args，调用open_plus_close_wifi执行scheduled wifi开关，
#           修复subprocess int类型报错，复用原版run_script规避GBK编码报错
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from datetime import datetime

# ===================== 时间配置区(可直接修改) =====================
TIME1_STR = "04:50:00"  # 时间1
TIME2_STR = "05:00:00"  # 时间2
# =================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# =================【docx指定统一文件夹路径】================
BASE_TYCLOUD_OLD = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\module"

FILE2_DEV_RECOG = os.path.join(BASE_TYCLOUD_OLD, "device_recognize.py")  # 文件2
FILE3_NET = os.path.join(BASE_TYCLOUD_OLD, "check_network_request.py")  # 文件3
FILE4_OPEN_WIFI = os.path.join(BASE_TYCLOUD_OLD, "open_plus_close_wifi.py")  # 文件4

START_TYCLOUD_PATH = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\module\start_tycloud\start_tycloud.py"
# ==============================================================================


# 完全复制代码1原版run_script，内部逻辑一行不动
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
    if filename in ("device_recognize.py", "check_network_request.py"):
        result = subprocess.run(cmd_list, capture_output=True, text=True, errors="replace")
        return result.returncode, result.stdout
    else:
        # open_plus_close_wifi.py / start_tycloud.py 业务脚本直接输出控制台
        result = subprocess.run(cmd_list, stdout=None, stderr=None)
        return result.returncode, ""


def get_time_extra_args():
    """
    1 获取系统时间
    2 判断系统时间是否在TIME1_STR与TIME2_STR之间
    返回变量1 extra_args：区间内=["2"]，不在区间=["1"]，返回字符串列表，匹配代码1调用格式
    """
    now_time = datetime.now().time()
    time1 = datetime.strptime(TIME1_STR, "%H:%M:%S").time()
    time2 = datetime.strptime(TIME2_STR, "%H:%M:%S").time()
    if time1 <= now_time <= time2:
        extra_args = ["2"]
    else:
        extra_args = ["1"]
    return extra_args


def main():
    print("========== scheduled wifi switch workflow start ==========")
    # 获取变量1 extra_args（字符串列表）
    extra_args = get_time_extra_args()
    # 调用文件4 open_plus_close_wifi
    ret_code, out_text = run_script(FILE4_OPEN_WIFI, "scheduled call open_plus_close_wifi.py", extra_args=extra_args)
    print(f"open_plus_close_wifi execute completed, return code={ret_code}")
    print("========== scheduled wifi switch workflow finished ==========")


if __name__ == "__main__":
    main()
