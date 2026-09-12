import subprocess
import os


def git_remote_override_local(repo_cwd: str) -> None:
    """
    远程仓库强制覆盖本地文件
    :param repo_cwd: Git仓库根目录(包含.git的文件夹绝对路径)
    """
    # 前置校验，参考git_auto_sync0模块
    if not os.path.isdir(repo_cwd):
        raise FileNotFoundError(f"Git仓库路径不存在！\nrepo_cwd = {repo_cwd}")
    git_dot_git = os.path.join(repo_cwd, ".git")
    if not os.path.isdir(git_dot_git):
        raise FileNotFoundError(f"该目录下没有.git文件夹，不是Git仓库！\n{git_dot_git}")

    print("==== 远程覆盖本地开始 ====")
    print(f"Git执行仓库目录: {repo_cwd}")
    print("⚠️ 警告：本操作会丢弃本地所有未提交修改！\n")

    print("[1/3] git fetch origin")
    ret_fetch = subprocess.run(["git", "fetch", "origin"], cwd=repo_cwd)
    if ret_fetch.returncode != 0:
        print("git fetch failed")
        raise SystemExit(1)

    # 直接写 origin/main，不再依赖 origin/HEAD，规避指针损坏问题
    print("[2/3] git reset --hard origin/main")
    ret_reset = subprocess.run(
        ["git", "reset", "--hard", "origin/main"], cwd=repo_cwd)
    if ret_reset.returncode != 0:
        print("git reset failed")
        raise SystemExit(1)

    print("[3/3] git clean -fd")
    subprocess.run(["git", "clean", "-fd"], cwd=repo_cwd)

    print("\n✅本地文件已同步为远程最新版本")
    print("==== 操作完成 ====")


if __name__ == "__main__":
    # ============仓库选择变量 1=main仓库，2=main_old仓库============
    SELECT_REPO = 2   # 修改这里切换目标git仓库
    # ==============================================================

    if SELECT_REPO == 1:
        GIT_REPOSITORY = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
    elif SELECT_REPO == 2:
        GIT_REPOSITORY = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
    else:
        raise ValueError(
            "SELECT_REPO只能填写1或者2！1代表005.490_main，2代表005.490_main_old")

    print(f"当前选择仓库编号 SELECT_REPO = {SELECT_REPO}")
    print(f"目标Git仓库路径：{GIT_REPOSITORY}")

    git_remote_override_local(repo_cwd=GIT_REPOSITORY)
