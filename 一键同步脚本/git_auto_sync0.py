import subprocess
from datetime import datetime
import os


def git_auto_sync(commit_prefix: str, repo_cwd: str) -> None:
    """
    执行完整Git一键同步流程
    :param commit_prefix: 提交注释前缀
    :param repo_cwd: Git仓库根目录(包含.git的文件夹绝对路径)
    """
    # 增加前置校验：判断仓库路径是否真实存在
    if not os.path.isdir(repo_cwd):
        raise FileNotFoundError(f"Git仓库路径不存在！\nrepo_cwd = {repo_cwd}")
    git_dot_git = os.path.join(repo_cwd, ".git")
    if not os.path.isdir(git_dot_git):
        raise FileNotFoundError(f"该目录下没有.git文件夹，不是Git仓库！\n{git_dot_git}")

    print("==== Git一键同步开始 ====")
    print(f"Git执行仓库目录: {repo_cwd}")
    print("确认 VSCode 已保存全部修改到磁盘\n")

    print("\n[2/4] git add . 添加全部改动")
    subprocess.run(["git", "add", "."], cwd=repo_cwd)

    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    commit_msg = f"{commit_prefix}_{now_str}"
    print(f"\n[3/4] git commit -m \"{commit_msg}\"")
    ret_commit = subprocess.run(
        ["git", "commit", "-m", commit_msg], cwd=repo_cwd)

    if ret_commit.returncode != 0:
        print("No changes detected; nothing to commit or push")
        print("==== Script finished ====")
        input("按回车退出...")
        raise SystemExit(0)

    print("\n[4/4] git push 推送至远程仓库")
    ret_push = subprocess.run(["git", "push", "-f"], cwd=repo_cwd)

    if ret_push.returncode != 0:
        print("git push failed")
        input("按回车退出...")
        raise SystemExit(1)

    print("\nSync completed")
    print("==== Git sync finished ====")


if __name__ == "__main__":
    TEST_REPO = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
    git_auto_sync("old.主任务_1.1.1.09008", repo_cwd=TEST_REPO)
