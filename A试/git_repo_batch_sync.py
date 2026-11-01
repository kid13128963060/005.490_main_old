# 版本:V1.1.1


import os
import sys
import subprocess
from Combination_Module.vscode_activate_with_keys import vscode_activate_with_keys
from Combination_Module.git_auto_sync import git_auto_sync
from Combination_Module.read_excel_const import read_simulator_cell
from Combination_Module.run_python_script import run_python_script, run_script_capture, run_script_get_stdout

# 提交说明
use_prefix = "工脑1031_18"
# 仓库路径
REPO_1 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
REPO_2 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# 普通推送
force_push_switch = False
select_repo_value = 3
repo_list: list[str] = []

vscode_activate_with_keys()
# 分支分开调用
if select_repo_value == 1:
    repo_path = REPO_1
    print("✅ 选择仓库:005.490_main")
    git_auto_sync(use_prefix, repo_cwd=repo_path, force_push=force_push_switch)
elif select_repo_value == 2:
    repo_path = REPO_2
    print("✅ 选择仓库:005.490_main_old")
    git_auto_sync(use_prefix, repo_cwd=repo_path, force_push=force_push_switch)
elif select_repo_value == 3:
    print("✅ 选择:一次性处理全部两个仓库(005.490_main + 005.490_main_old)")
    # 直接调用两次，分别传字符串
    git_auto_sync(use_prefix, repo_cwd=REPO_1, force_push=force_push_switch)
    git_auto_sync(use_prefix, repo_cwd=REPO_2, force_push=force_push_switch)
else:
    raise ValueError("仅支持选项1、2、3")
