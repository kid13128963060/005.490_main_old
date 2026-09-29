# -*- coding: utf-8 -*-
# version: V1.5
# 功能: 根据脚本扩展名自动选择执行方式，支持py脚本与ps1脚本；
#       capture_output_flag标记控制是否捕获标准输出；
#       target_script_name脚本基础名称可配置，也支持运行时用户手动输入；
#       capture_output_flag为True捕获输出，False直接透传控制台输出；
#       无论是否捕获输出均返回CompletedProcess对象。
# 注意: script_path为待执行脚本完整绝对路径；
#       check=False，不会因脚本非0返回码抛出异常；
#       .py后缀调用python执行，.ps1后缀调用powershell执行。
import os
import subprocess

from module.find_target_script import find_target_script

# ========= 配置项 =========
target_script_name = "open_plus_close_wifi"  # 默认脚本基础名称（不带后缀）
# ==========================


def run_python_script(script_path, capture_output_flag=False):
    """
    根据文件后缀自动选择执行命令，支持 .py 与 .ps1
    :param script_path: 脚本完整绝对路径
    :param capture_output_flag: True捕获输出，False直接输出到控制台
    :return: CompletedProcess对象
    """
    # 获取文件扩展名，小写统一处理
    ext = os.path.splitext(script_path)[1].lower()
    if ext == ".py":
        cmd = ["python", script_path]
    elif ext == ".ps1":
        # powershell执行ps1脚本命令
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path]
    else:
        raise ValueError(f"不支持的脚本后缀：{ext}，仅支持 .py / .ps1")

    if capture_output_flag:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    else:
        result = subprocess.run(cmd, check=False)
    return result


if __name__ == "__main__":
    # 用户手动输入脚本名称，为空则使用配置项默认值
    input_name = input("请输入要查找的脚本名称（不带后缀）：").strip()
    if input_name:
        target_script_name = input_name

    # 调用find_target_script搜索脚本，返回值赋值给script_path
    script_path = find_target_script(target_script_name=target_script_name, recursive=True)
    print(f"从文件2获取得到脚本路径：{script_path}")

    if script_path is not None:
        try:
            proc = run_python_script(script_path, capture_output_flag=False)
            print(f"脚本执行返回码：{proc.returncode}")
        except ValueError as e:
            print(f"执行异常：{e}")
