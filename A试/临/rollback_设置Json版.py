# V1.0.1 增加仓库选择，支持外部目录运行
import subprocess
import os

# ============仓库选择变量 1=main仓库，2=main_old仓库============
SELECT_REPO = 2   # 修改这里切换目标git仓库
# ==============================================================

if SELECT_REPO == 1:
    GIT_REPOSITORY = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
elif SELECT_REPO == 2:
    GIT_REPOSITORY = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
else:
    raise ValueError("SELECT_REPO只能填写1或者2！1代表005.490_main，2代表005.490_main_old")

# 定义目标提交哈希
TARGET_COMMIT_HASH = "94ca24d9ad4ea80450023f27d5fa05e5f3a13720"

# 固定进程工作目录为路径1，兼容VS Code跨目录启动
ROOT_WORK_DIR = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1"
os.chdir(ROOT_WORK_DIR)


def run_git_command(cmd: list[str], cwd: str):
    """执行git命令，指定仓库工作目录，出错抛出异常"""
    print(f"执行命令: {' '.join(cmd)}")
    print(f"git执行工作目录(cwd参数): {cwd}")
    print(f"Python进程当前工作目录(os.cwd): {os.getcwd()}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(
            f"命令失败:\nstdout:{result.stdout}\nstderr:{result.stderr}")
    print(result.stdout)


if __name__ == "__main__":
    try:
        print(f"当前选择仓库编号 SELECT_REPO = {SELECT_REPO}")
        print(f"目标Git仓库路径：{GIT_REPOSITORY}")
        print("⚠️警告：将会清空本地未提交改动，强制覆盖远程main分支，仅单人仓库使用！")

        run_git_command(["git", "fetch", "origin"], cwd=GIT_REPOSITORY)
        run_git_command(["git", "reset", "--hard",
                        TARGET_COMMIT_HASH], cwd=GIT_REPOSITORY)
        run_git_command(["git", "push", "origin", "main",
                        "--force"], cwd=GIT_REPOSITORY)

        print("✅ 已回退至 指定历史分支，并强制推送远程main")
    except Exception as e:
        print(f"❌ 回滚失败：{e}")
