import sys
import os
import subprocess
import time

# =====================配置区=====================
run_mode = 2
kill_exe_list_path = r"E:\备份盘\8000_大文件夹_同\009_备份文件夹_同\list\kill_exe_list.txt"
# 外部脚本完整路径
SAVE_CLOSE_SCRIPT = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\Combination_Module\save_close_word_notepad_before_shutdown.py"
# ================================================


from Combination_Module.vscode_activate_with_keys import vscode_activate_with_keys

# 读取exe进程清单
proc_names = []
if os.path.exists(kill_exe_list_path):
    with open(kill_exe_list_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                proc_names.append(line)
print(f"读取到 {len(proc_names)} 个待关闭exe进程")


if run_mode == 1:
    print("【测试模式】模拟执行关闭流程")
    print(f"【测试模式】模拟调用外部脚本：{SAVE_CLOSE_SCRIPT} →全部保存关闭Word、记事本")
    for p in proc_names:
        print(f"【测试模式】模拟处理进程：{p}")
        if p.lower() == "code.exe":
            print("【测试模式】模拟执行 vscode_activate_with_keys() VSCode全部保存")
    print("【测试模式】模拟执行taskkill强制结束exe进程")

else:
    print("\n===== 第一步：调用外部脚本，全部保存并关闭Word、记事本 =====")
    if os.path.exists(SAVE_CLOSE_SCRIPT):
        ret = subprocess.run([sys.executable, SAVE_CLOSE_SCRIPT])
        print(f"外部脚本执行返回码：{ret.returncode}")
        time.sleep(1.0)
    else:
        print(f"⚠️ 外部脚本不存在：{SAVE_CLOSE_SCRIPT}")

    print("\n===== 第二步：对清单内exe，先执行对应保存动作 =====")
    for proc in proc_names:
        if proc.lower() == "code.exe":
            print(f"✅ VSCode，执行 vscode_activate_with_keys() 全部保存")
            ret = vscode_activate_with_keys()
            print(f"vscode_activate_with_keys 返回值={ret}")
            time.sleep(1.2)

    print("\n===== 第三步：强制结束清单内所有exe进程 =====")
    for proc in proc_names:
        print(f"正在强制结束进程：{proc}")
        subprocess.run(["taskkill", "/f", "/t", "/im", proc], shell=False)
