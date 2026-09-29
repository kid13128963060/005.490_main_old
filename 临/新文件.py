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

from Combination_Module.run_python_script import run_python_script

# 方式A：不捕获输出，脚本print直接打印控制台
res1 = run_python_script("open_plus_close_wifi", capture_output_flag=False)


# ==========顶部配置区（放在一级根目录app_root上方）==========
# module脚本名字典，集中维护module目录全部脚本文件名，key从0顺序递增
module_script_dict = {
    0: "read_excel_once.py",
    1: "open_plus_close_wifi.py",
    2: "check_network_request_True.py",
}
# =========================================================

# 一级根目录：App总根目录
app_root = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App"
# 新增二级根路径：module文件夹专用根路径
module_root = os.path.join(app_root, "module")

# ps1脚本，使用一级app_root拼接
path1_ps1 = os.path.join(app_root, "云端_本地配置_互传", "本地覆盖云端配置.ps1")
# start_tycloud脚本，使用一级app_root拼接
path3_py = os.path.join(app_root, "start_tycloud", "start_tycloud.py")

# --------------------------
# 根据字典自动生成module脚本完整路径列表，key和列表下标严格一一对应
# 后续字典增加key，此列表自动变长，不需要手动新增path变量
module_path_list = []
sorted_keys = sorted(module_script_dict.keys())
for k in sorted_keys:
    full_path = os.path.join(module_root, module_script_dict[k])
    module_path_list.append(full_path)
# --------------------------

# 索引映射（和字典key保持一致）
# module_path_list[0] → read_excel_once.py
# module_path_list[1] → open_plus_close_wifi.py
# module_path_list[2] → check_network_request_True.py


# 封装执行python脚本的函数
