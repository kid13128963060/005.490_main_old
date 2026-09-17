# -*- coding: utf-8 -*-
# version: V1.1
# 修复点：移除capture_output捕获输出；子进程直接继承控制台，避免特殊字符编码报错；保证start_tycloud正常启动

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# 文件4完整绝对路径
FILE4 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\start_tycloud\start_tycloud.py"


def run_script(path, label):
    print(f"\n---- 执行{label}  {path} ----")
    if not os.path.exists(path):
        print(f"错误：文件不存在 {path}")
        return -1
    cmd_list = [sys.executable, path]
    # stdout=None、stderr=None：子进程直接输出到当前控制台，不捕获，彻底避开编码转换报错
    result = subprocess.run(cmd_list, stdout=None, stderr=None)
    return result.returncode


def main():
    print("========== 单独启动文件4 start_tycloud.py ==========")
    ret = run_script(FILE4, "文件4(天翼云盘启动脚本)")
    print(f"\n========== 文件4执行结束，返回码={ret} ==========")


if __name__ == "__main__":
    main()
