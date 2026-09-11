# 说明本地修改上传推送
from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync

EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"

if __name__ == "__main__":
    # 读取excel常量
    CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
    print(f"读取到模拟器标识：{CELL_READ_CONST}")

    # 条件判断选择提交前缀
    if CELL_READ_CONST == "家脑模拟器":
        CommitPrefix = "家脑_old_1.1.1.09002"
    elif CELL_READ_CONST == "工脑模拟器":
        CommitPrefix = "工脑_old_1.1.1.09011"
    else:
        raise ValueError(f"未知模拟器类型：{CELL_READ_CONST}，无法选择git提交前缀")

    print(f"选定提交前缀：{CommitPrefix}")
    # 执行完整git同步
    git_auto_sync(CommitPrefix)
