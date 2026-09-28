# 版本: V3.2
# 功能: 指定app_root根目录，自动遍历目录，
#       自动搜索目标脚本，根据脚本扩展名自动选择执行器，
#       支持ps1与py；主脚本支持命令行参数action‑code，
#       传入action‑code则转发数字给子脚本，未传入则传递遍历提取的文件名，
#       使用遍历得到的脚本路径执行调用，不硬编码拼接脚本路径，
#       不做脚本存在校验，脚本执行成功后直接跳出全部遍历，
#       维护名单：名单内脚本输出直接透传控制台不捕获，规避管道阻塞、
#       GBK/非utf‑8编码崩溃；名单外脚本捕获原始字节，容错解码替换非法字节
# 注意: recursive控制是否递归遍历子文件夹，
#       delay控制两次调用脚本之间的间隔时间，
#       no_capture_script_list名单内脚本直接透传控制台，
#       ps1后缀调用powershell，py后缀调用python解释器，
#       命令行示例：python root_file_batch_run.py --action-code=1
import argparse
import os
import subprocess
import time

# ========= 解析主脚本命令行参数 =========
parser = argparse.ArgumentParser()
parser.add_argument(
    "--action-code",
    type=int,
    default=None,
    help="转发给子脚本的action_code数字，不传则传递遍历得到的文件名",
)
args = parser.parse_args()
forward_action_code = args.action_code

# ========= 配置项 =========
app_root = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App"
recursive = True  # 是否遍历子文件夹，True开启，False仅扫描一级目录
delay = 0.05  # 每次调用脚本间隔秒数，防止调用过快
target_script_name = "open_plus_close_wifi"  # 不带后缀的脚本基础名称
# 名单内脚本：stdout/stderr直接透传到控制台，不捕获输出，避免阻塞、编码报错
no_capture_script_list = ["open_plus_close_wifi.py", "start_tycloud.py"]
# ==========================

# 第一步：遍历查找脚本，匹配 .ps1 / .py 后缀，获取真实路径
found_script_path = None
for walk_root, walk_dirs, walk_files in os.walk(app_root):
    for f in walk_files:
        base_name, ext = os.path.splitext(f)
        if base_name == target_script_name and ext in (".ps1", ".py"):
            found_script_path = os.path.join(walk_root, f)
            break
    if found_script_path is not None:
        break
    if not recursive:
        break

# 第二步：遍历所有普通业务文件，提取文件名，调用找到的脚本
stop_all = False
for root, dirs, files in os.walk(app_root):
    for filename in files:
        # 收到停止标记，立刻退出
        if stop_all:
            break
        # 跳过目标脚本本身，不要处理这个脚本文件
        if found_script_path and filename == os.path.basename(found_script_path):
            continue

        file_path = os.path.join(root, filename)
        name_no_ext = os.path.splitext(filename)[0]

        print(f"\n文件路径: {file_path}")
        print(f"文件名(无后缀): {name_no_ext}")

        # 判断主脚本是否接收到action‑code参数，决定转发参数
        if forward_action_code is not None:
            call_arg = str(forward_action_code)
            print(f"主脚本命令行获得action‑code，向子脚本传递参数:{call_arg}")
        else:
            call_arg = name_no_ext
            print(f"未设置主脚本action‑code，向子脚本传递文件名:{call_arg}")

        # 处理找不到脚本的情况，防止None传入subprocess产生类型报错
        if found_script_path is not None:
            try:
                _, script_ext = os.path.splitext(found_script_path)
                script_file_name = os.path.basename(found_script_path)
                # 判断是否属于直接透传输出的脚本名单
                use_direct_console = script_file_name in no_capture_script_list

                if script_ext == ".ps1":
                    if use_direct_console:
                        ret = subprocess.run(
                            [
                                "powershell.exe",
                                "-ExecutionPolicy",
                                "Bypass",
                                "-File",
                                found_script_path,
                                call_arg,
                            ],
                            check=False,
                            shell=False,
                            stdout=None,
                            stderr=None,
                        )
                    else:
                        ret = subprocess.run(
                            [
                                "powershell.exe",
                                "-ExecutionPolicy",
                                "Bypass",
                                "-File",
                                found_script_path,
                                call_arg,
                            ],
                            check=False,
                            shell=False,
                            capture_output=True,
                        )
                elif script_ext == ".py":
                    if use_direct_console:
                        # 直接继承控制台输出，不捕获输出，解决脚本无输出、编码崩溃
                        ret = subprocess.run(
                            ["python", found_script_path, call_arg],
                            check=False,
                            shell=False,
                            stdout=None,
                            stderr=None,
                        )
                    else:
                        ret = subprocess.run(
                            ["python", found_script_path, call_arg],
                            check=False,
                            shell=False,
                            capture_output=True,
                        )
                else:
                    print(f"不支持的脚本后缀:{script_ext}，跳过调用")
                    time.sleep(delay)
                    continue

                # 只有非透传模式，才做字节容错解码并打印输出
                if not use_direct_console:
                    stdout_text = ret.stdout.decode("utf8", errors="replace")
                    stderr_text = ret.stderr.decode("utf8", errors="replace")
                    if stdout_text.strip():
                        print(f"【子脚本输出】\n{stdout_text}")
                    if stderr_text.strip():
                        print(f"【子脚本错误输出】\n{stderr_text}")
                else:
                    print("【透传控制台模式】脚本输出直接打印控制台，不捕获缓存")

                # 返回码0代表脚本业务执行成功，设置标记跳出所有循环
                if ret.returncode == 0:
                    print("脚本执行成功，终止全部文件遍历")
                    stop_all = True
                    break

            except Exception as e:
                print(f"调用脚本发生异常: {e}")
        else:
            print("提示：未遍历找到目标ps1/py脚本")

        time.sleep(delay)
    if stop_all or (not recursive):
        break
