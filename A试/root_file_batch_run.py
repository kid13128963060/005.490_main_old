# 版本: V2.9
# 功能: 指定app_root根目录，自动遍历目录，
#       自动搜索目标脚本，根据脚本扩展名自动选择执行器，
#       支持ps1与py，再遍历普通文件提取文件名，
#       使用遍历得到的脚本路径执行调用，不硬编码拼接脚本路径，
#       不做脚本存在校验，脚本执行成功后直接跳出全部遍历，
#       获取子脚本原始字节输出，采用容错解码，
#       避免子脚本输出非utf‑8字节直接引发主脚本崩溃
# 注意: recursive控制是否递归遍历子文件夹，
#       delay控制两次调用脚本之间的间隔时间，
#       ps1后缀调用powershell，py后缀调用python解释器
import os
import subprocess
import time

# ========= 配置项 =========
app_root = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App"
recursive = True  # 是否遍历子文件夹，True开启，False仅扫描一级目录
delay = 0.05  # 每次调用脚本间隔秒数，防止调用过快
target_script_name = "open_plus_close_wifi"  # 不带后缀的脚本基础名称
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

        # 处理找不到脚本的情况，防止None传入subprocess产生类型报错
        if found_script_path is not None:
            try:
                _, script_ext = os.path.splitext(found_script_path)
                if script_ext == ".ps1":
                    ret = subprocess.run(
                        [
                            "powershell.exe",
                            "-ExecutionPolicy",
                            "Bypass",
                            "-File",
                            found_script_path,
                            name_no_ext,
                        ],
                        check=False,
                        shell=False,
                        capture_output=True,
                        # 关闭text=True，不指定编码，直接获取bytes原始字节
                    )
                elif script_ext == ".py":
                    ret = subprocess.run(
                        ["python", found_script_path, name_no_ext],
                        check=False,
                        shell=False,
                        capture_output=True,
                    )
                else:
                    print(f"不支持的脚本后缀:{script_ext}，跳过调用")
                    time.sleep(delay)
                    continue

                # 容错解码：优先utf‑8，无法解析字节直接替换符号，不抛异常
                stdout_text = ret.stdout.decode("utf‑8", errors="replace")
                stderr_text = ret.stderr.decode("utf‑8", errors="replace")

                # 打印子脚本输出、错误信息，便于调试业务脚本
                if stdout_text.strip():
                    print(f"【子脚本输出】\n{stdout_text}")
                if stderr_text.strip():
                    print(f"【子脚本错误输出】\n{stderr_text}")

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
