from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync


EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"
CommitPrefix = "old.一键保存关闭V1.0.03"

# ========= Git仓库绝对路径，必须 r"" 原始字符串，不要去掉r！ =========
GIT_REPOSITORY = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# =================================================================


if __name__ == "__main__":
    CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
    print(f"读取到模拟器标识：{CELL_READ_CONST}")

    print(f"选定提交前缀：{CommitPrefix}")
    git_auto_sync(CommitPrefix, repo_cwd=GIT_REPOSITORY)
