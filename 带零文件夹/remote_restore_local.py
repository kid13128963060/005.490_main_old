import subprocess
import os


def git_remote_override_local() -> None:
    print("==== 远程覆盖本地开始 ====")
    print("⚠️ 警告：本操作会丢弃本地所有未提交修改！\n")

    # 【可选】锁定工作目录，防止执行路径出错
    # REPO_ROOT = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
    # os.chdir(REPO_ROOT)

    print("[1/3] git fetch origin")
    ret_fetch = subprocess.run(["git", "fetch", "origin"])
    if ret_fetch.returncode != 0:
        print("git fetch failed")
        raise SystemExit(1)

    # 直接写 origin/main，不再依赖 origin/HEAD，规避指针损坏问题
    print("[2/3] git reset --hard origin/main")
    ret_reset = subprocess.run(["git", "reset", "--hard", "origin/main"])
    if ret_reset.returncode != 0:
        print("git reset failed")
        raise SystemExit(1)

    print("[3/3] git clean -fd")
    subprocess.run(["git", "clean", "-fd"])
    print("\n✅本地文件已同步为远程最新版本")
    print("==== 操作完成 ====")


if __name__ == "__main__":
    git_remote_override_local()
