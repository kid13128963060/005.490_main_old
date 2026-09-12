from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync


EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"
CommitPrefix = "old.local_first_git_pushV1.0.05"

# ============仓库选择变量 1=main仓库，2=main_old仓库============
SELECT_REPO = 2   # 修改这里切换目标git仓库
# ==============================================================

if SELECT_REPO == 1:
    GIT_REPOSITORY = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
elif SELECT_REPO == 2:
    GIT_REPOSITORY = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
else:
    raise ValueError("SELECT_REPO只能填写1或者2！1代表005.490_main，2代表005.490_main_old")


if __name__ == "__main__":
    CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
    print(f"读取到模拟器标识：{CELL_READ_CONST}")

    print(f"选定提交前缀：{CommitPrefix}")
    print(f"当前选择仓库编号 SELECT_REPO = {SELECT_REPO}")
    print(f"目标Git仓库路径：{GIT_REPOSITORY}")

    # ⚠️必须传入repo_cwd参数，不能省略！
    git_auto_sync(CommitPrefix, repo_cwd=GIT_REPOSITORY)
