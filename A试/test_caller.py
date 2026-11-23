import subprocess


def call_py_script(
    py_script_fullpath: str = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\module\batch_open_file_list.py",
    *args
) -> int:
    """
    通用调用外部py脚本
    :param py_script_fullpath: 被调用py完整路径
    :param args: 可变参数列表，不传就是不给脚本传任何参数
    :return: 子进程返回码
    """
    cmd = ["python", py_script_fullpath, *args]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
    return res.returncode


if __name__ == "__main__":
    # ====================== 配置区 ======================
    # 整合为一个脚本路径变量，切换脚本只改这一行
    script_path = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\module\batch_open_file_list.py"

    arg_single = r"F:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\启动热点"
    arg_m1 = "第一个参数"
    arg_m2 = "第二个参数"
    arg_m3 = "第三个参数"
    # ===================================================

    run_mode = 1  # 1=无参 | 2=单参 | 3=多参
    ret = -1

    if run_mode == 1:
        ret = call_py_script(script_path)
    elif run_mode == 2:
        ret = call_py_script(script_path, arg_single)
    elif run_mode == 3:
        ret = call_py_script(script_path, arg_m1, arg_m2, arg_m3)
    else:
        print("run_mode 只能是 1 / 2 / 3")

    print("返回码：", ret)
