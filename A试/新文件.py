# 版本:V1.1.14
# 功能:调用路径1ps1脚本、path2_py、path3_py、path4_py；先执行ps1，
# 延时后依次执行py脚本；捕获path2_py读取Excel得到模拟器标识字符串，
# 根据不同模拟器标识执行不同等待时长，最后执行wifi开关脚本
# 需求：设置一级app_root项目根目录，额外新增二级module_root根路径，
# module目录下脚本使用二级根路径拼接
# 修改说明：V1.0.14 module脚本名字典放置在一级根目录app_root定义之上；
# 不再手动逐个定义pathX_module_py变量；根据字典自动生成路径列表；
# Path下标数字与字典key顺序一一对应；后续新增字典条目，路径自动扩展，无需手动新增path变量

import os
import sys
import subprocess

from Combination_Module.git_auto_sync0 import git_auto_sync
from Combination_Module.read_excel_const import read_simulator_cell

from Combination_Module.vscode_activate_with_keys import vscode_activate_with_keys

vscode_activate_with_keys()
