# 版本:V1.0.09
# 功能:调用路径1ps1脚本、path2_py、path3_py、path4_py；先执行ps1，
# 延时后依次执行py脚本；捕获path2_py读取Excel得到模拟器标识字符串，
# 根据不同模拟器标识执行不同等待时长，最后执行wifi开关脚本
# 需求：设置一级app_root项目根目录，额外新增二级module_root根路径，
# module目录下脚本使用二级根路径拼接
# 修改说明：V1.0.09 module脚本名字典放置在一级根目录app_root定义之上，
# 使用字典集中维护module下全部脚本文件名

import os
import subprocess
import time

# ==========顶部配置区（放在一级根目录app_root上方）==========
# module脚本名字典，集中维护module目录全部脚本文件名
module_script_dict = {
    "read_excel": "read_excel_once.py",
    "wifi_operate": "open_plus_close_wifi.py",
    "net_check": "check_network_request_True.py",
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

# 通过字典key拼接完整module脚本路径
path2_py = os.path.join(module_root, module_script_dict["read_excel"])
path4_py = os.path.join(module_root, module_script_dict["wifi_operate"])
path5_py = os.path.join(module_root, module_script_dict["net_check"])


# 封装执行python脚本的函数
def run_python_script(script_path, capture_output_flag=False):
    # capture_output_flag=True时捕获标准输出，用于获取脚本输出字符串
    if capture_output_flag:
        result = subprocess.run(
            ["python", script_path], capture_output=True, text=True, check=False
        )
    else:
        # 不捕获输出时，依然返回CompletedProcess，不再返回None
        result = subprocess.run(["python", script_path], check=False)
    return result


# 本地覆盖云端配置
subprocess.run(["pwsh", "-ExecutionPolicy", "Bypass", "-File", path1_ps1], check=False)

time.sleep(5)  # 等待5秒，确保ps1脚本执行完成

# 获取模拟器标识
CELL_READ_CONST = run_python_script(path2_py, capture_output_flag=True).stdout.strip()
print(CELL_READ_CONST)

# check_network_request_True.py
net_ok = run_python_script(path5_py, capture_output_flag=True).stdout.strip()

print(f"net_ok：{net_ok}")
run_python_script(path4_py)

# 文档要求：变量5 net_ok=False，则文件4变量6 action_code=1
if not net_ok:
    print("检测结果：无网络(net_ok=False)，执行文件4 open_plus_close_wifi")
    run_python_script(path4_py)
else:
    print("检测结果：网络正常，跳过执行文件4 open_plus_close_wifi")

# start_tycloud
run_python_script(path3_py)

if CELL_READ_CONST == "家脑模拟器":
    print("家脑模拟器标识字符串匹配成功")
    time.sleep(5)
elif CELL_READ_CONST == "工脑模拟器":
    print("工脑模拟器标识字符串匹配成功")
    time.sleep(35)
else:
    print("模拟器标识字符串不匹配")
