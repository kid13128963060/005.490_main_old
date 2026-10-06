# 版本: V1.8测试Ok | 功能: 根据扩展名自动执行脚本，支持py与ps1文件；
# 变更记录 V1.8:新增run_script_capture包装函数，提供更稳定的返回值
# 变更记录 V1.7:新增extra_args支持向脚本传递命令行参数
# 变更 V1.8‑STR: 新增 run_script_get_stdout() 直接返回strip后的stdout字符串
# 注意: 函数内部调用find_target_script获取完整脚本路径；
#       py使用python命令执行，ps1调用pwsh命令执行；
#       check=False，不会因脚本非0返回码抛出异常。

import os
import subprocess
from subprocess import CompletedProcess
from module.find_target_script import find_target_script


# ========== 原版 run_python_script V1.7 保持原样，不要修改 ==========
def run_python_script(target_script_name, capture_output_flag=False, extra_args=None):
    if extra_args is None:
        extra_args = []
    script_path = find_target_script(target_script_name=target_script_name, recursive=True)
    if script_path is None:
        return None

    ext = os.path.splitext(script_path)[1]
    if ext == ".py":
        cmd = ["python", script_path] + extra_args
    elif ext == ".ps1":
        cmd = ["pwsh", "-ExecutionPolicy", "Bypass", "-File", script_path] + extra_args
    else:
        return None

    if capture_output_flag:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    else:
        result = subprocess.run(cmd, check=False)
    return result


# ========== 包装函数1：返回CompletedProcess对象（保留，可选继续使用） ==========
def run_script_capture(target_script_name, extra_args=None) -> CompletedProcess:
    """
    固定开启 capture_output_flag=True；
    找不到脚本不会返回None，返回一个空的模拟CompletedProcess；
    返回对象永远有 .stdout .stderr .returncode 属性，消除Pylance None警告
    """
    proc = run_python_script(target_script_name=target_script_name, capture_output_flag=True, extra_args=extra_args)

    if proc is None:
        print(f"错误：未找到 {target_script_name} 脚本")
        dummy_proc = CompletedProcess(args=[], returncode=-1, stdout="", stderr="")
        return dummy_proc
    return proc


# ========== 【新增】直接返回字符串版本 ==========
def run_script_get_stdout(target_script_name, extra_args=None) -> str:
    """
    直接返回已经 strip() 处理后的stdout字符串
    :param target_script_name: 脚本短名不带后缀
    :param extra_args: 命令行参数列表
    :return: str；脚本找不到/异常返回空字符串""，自动strip去除换行首尾空格
    """
    proc = run_python_script(target_script_name=target_script_name, capture_output_flag=True, extra_args=extra_args)
    # 脚本文件不存在
    if proc is None:
        print(f"错误：未找到 {target_script_name} 脚本")
        return ""
    # 打印stderr错误信息，方便调试，但是不影响返回的stdout
    err_text = proc.stderr.strip()
    if err_text:
        print(f"[{target_script_name}] stderr: {err_text}")
    # 返回去除换行、首尾空白的字符串
    return str(proc.stdout).strip()
