# 说明本地修改上传推送local_first_git_push_V1.0.002
from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync

EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"

if __name__ == "__main__":
    # 读取excel常量
    CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
    print(f"读取到模拟器标识：{CELL_READ_CONST}")

    # 固定提交前缀
    CommitPrefix = "old.测试推送_1.1.1.09007"
    print(f"选定提交前缀：{CommitPrefix}")
    # 执行完整git同步
    git_auto_sync(CommitPrefix)
