import subprocess


def git_remote_override_local() -> None:
    """
    仅用远程仓库覆盖本地，不提交、不推送到远程
    流程：获取远程最新 -> 硬重置本地分支 -> 清理本地未跟踪文件
    """
    print("==== 远程覆盖本地开始 ====")
    print("⚠️ 警告：本操作会丢弃本地所有未提交修改！\n")

    # 1. 获取远程最新分支信息（只下载，不合并）
    print("[1/3] git fetch origin")
    ret_fetch = subprocess.run(
        ["git", "fetch", "origin"], capture_output=False)
    if ret_fetch.returncode != 0:
        print("git fetch failed")
        input("按回车退出...")
        raise SystemExit(1)

    # 2. 硬重置本地分支，完全对齐远程分支，丢弃本地改动
    print("\n[2/3] git reset --hard origin/HEAD")
    ret_reset = subprocess.run(
        ["git", "reset", "--hard", "origin/HEAD"], capture_output=False)
    if ret_reset.returncode != 0:
        print("git reset failed")
        input("按回车退出...")
        raise SystemExit(1)

    # 3. 清理本地未跟踪的文件和文件夹（可选，不需要就注释掉）
    print("\n[3/3] git clean -fd")
    ret_clean = subprocess.run(["git", "clean", "-fd"], capture_output=False)
    if ret_clean.returncode != 0:
        print("git clean failed")
        input("按回车退出...")
        raise SystemExit(1)

    print("\n✅ 本地文件已同步为远程最新版本")
    print("==== 操作完成 ====")


if __name__ == "__main__":
    git_remote_override_local()
