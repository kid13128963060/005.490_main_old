import subprocess

ps1_path = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\云端_本地配置_互传\云端覆盖本地配置.ps1"


def run_ps1_script(ps1_path):
    """
    执行指定路径的ps1脚本，转换返回码：PS返回0 → 函数返回1，其他错误码不变
    :param ps1_path: ps1脚本完整路径
    :return: (stdout, stderr, final_code)
    """
    # 调用powershell执行脚本
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1_path],
        capture_output=True,
        text=True
    )
    # ========== 转换返回码 ==========
    # 原始返回码0（PS脚本成功） → 修改为1；其他错误码保持原样
    if result.returncode == 0:
        final_code = 1
    else:
        final_code = result.returncode

    return result.stdout, result.stderr, final_code


# 调用函数执行Ps1脚本，并获取返回值
stdout, stderr, final_code = run_ps1_script(ps1_path)

# 打印结果
print("标准输出：", stdout)
print("错误信息：", stderr)
print("转换后的返回码：", final_code)
