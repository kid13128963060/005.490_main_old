# 版本: V6.4 | 功能:设备识别工作流；读取excel获取模拟器标识，执行设备识别、网络检测，
#       根据网络状态控制wifi开关；工脑模拟器启动Ditto，最后执行ps1配置脚本；
# 变更记录：V6.1.1 修改BASE_TYCLOUD_OLD路径
# 变更记录：V6.2 基础版本
# 变更记录：V6.3 main函数末尾增加调用run_ps1_script函数，执行ps1脚本并打印输出与转换后返回码
# 变更记录：V6.4 删除本文件内部旧版run_python_script、run_ps1_script、run_script；
#       导入外部run_python_script函数；全部脚本改用短名调用；ps1脚本使用新函数执行；
#       增加脚本查找失败None防护；修复Pylance对stdout类型推断报错，所有stdout增加str()转换
import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# 一级根目录：App总根目录
app_root = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App"

# 导入外部run_python_script（文件2 run_python_script.py）
from Combination_Module.run_python_script import run_python_script


def main():
    print("========== 设备识别工作流开始 ==========")

    # 获取模拟器标识 read_excel_once，捕获输出
    ret_read_excel = run_python_script("read_excel_once", capture_output_flag=True)
    if ret_read_excel is None:
        print("错误：未找到 read_excel_once 脚本，程序终止")
        return
    CELL_READ_CONST = str(ret_read_excel.stdout).strip()
    print(CELL_READ_CONST)

    # 步骤1：调用 device_recognize 设备识别，捕获输出解析DEV_RET标记
    ret_dev = run_python_script("device_recognize", capture_output_flag=True)
    if ret_dev is None:
        print("错误：未找到 device_recognize 脚本")
        current_device = None
    else:
        current_device = None
        out_dev = str(ret_dev.stdout)
        for line in out_dev.splitlines():
            if line.startswith("DEV_RET:"):
                val = line.split(":", 1)[1].strip()
                if val == "1":
                    current_device = 1
                elif val == "2":
                    current_device = 2
                else:
                    current_device = None
    print(f"【current_device】= {current_device}")

    # 步骤2：调用 check_network_request 网络检测，解析NET_RET标记获取net_ok
    ret_net = run_python_script("check_network_request", capture_output_flag=True)
    if ret_net is None:
        print("错误：未找到 check_network_request 脚本")
        net_ok = False
    else:
        net_ok = False
        out_net = str(ret_net.stdout)
        for line in out_net.splitlines():
            if line.startswith("NET_RET:"):
                val = line.split(":", 1)[1].strip()
                net_ok = val == "True"
    print(f"【net_ok】={net_ok}")

    # net_ok=False，执行open_plus_close_wifi
    if not net_ok:
        print("检测结果：无网络(net_ok=False)，执行文件4 open_plus_close_wifi")

        ret_wifi = run_python_script("open_plus_close_wifi", extra_args=["1"])
        if ret_wifi is None:
            print("警告：未找到 open_plus_close_wifi 脚本，wifi操作跳过")
    else:
        print("检测结果：网络正常，跳过执行文件4 open_plus_close_wifi")

    print("\n合并步骤执行完成，延时等待5秒……")
    time.sleep(5)

    print("\n>>>> 等待结束，执行路径1：start_tycloud.py天翼云盘脚本")
    ret_start_ty = run_python_script("start_tycloud")
    if ret_start_ty is None:
        print("警告：未找到 start_tycloud 脚本")

    if CELL_READ_CONST == "工脑模拟器":
        print("工脑模拟器标识字符串匹配成功")
        # 启动Ditto程序
        FILE5_Ditto = r"C:\Program Files\Ditto\Ditto.exe"
        if os.path.exists(FILE5_Ditto):
            subprocess.Popen(FILE5_Ditto)
        else:
            print(f"警告：Ditto程序不存在 {FILE5_Ditto}")
    else:
        print("模拟器标识字符串不匹配")

    print("启动天翼云盘")
    run_python_script("start_tycloud")
    print("等检天翼云盘同步完成")
    ret_sync_check = run_python_script("TyCloud_UIA_SyncStatusCheck")
    if ret_sync_check is None:
        print("警告：未找到 TyCloud_UIA_SyncStatusCheck 脚本")

    # V6.4改造：ps1脚本【云端覆盖本地配置】改用外部run_python_script函数调用
    print("\n---------- 开始调用run_python_script执行ps1脚本 ----------")
    ret_ps1 = run_python_script("云端覆盖本地配置", capture_output_flag=True)
    if ret_ps1 is None:
        print("错误：未找到【云端覆盖本地配置.ps1】脚本")
    else:
        print("标准输出：", str(ret_ps1.stdout))
        print("错误信息：", str(ret_ps1.stderr))
        print("ps1脚本原始返回码：", ret_ps1.returncode)
    print("---------- ps1脚本调用执行完毕 ----------")

    print("主脚本执行Ok")
    print("\n========== 设备识别工作流全部执行结束 ==========")


if __name__ == "__main__":
    main()
