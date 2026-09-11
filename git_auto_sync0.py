import subprocess
from datetime import datetime


def git_auto_sync(commit_prefix: str) -> None:
    """
    执行完整Git一键同步流程，等价参考docx里的powershell脚本
    :param commit_prefix: 提交注释前缀，由excel读取结果决定
    """
    print("==== Git一键同步开始 ====")
    print("确认 VSCode 已保存全部修改到磁盘\n")

    # 2 git add .
    print("\n[2/4] git add . 添加全部改动")
    subprocess.run(["git", "add", "."])

    # 3 git commit 拼接时间戳备注
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    commit_msg = f"{commit_prefix}_{now_str}"
    print(f"\n[3/4] git commit -m \"{commit_msg}\"")
    ret_commit = subprocess.run(["git", "commit", "-m", commit_msg])

    # commit返回非0：无变更，正常结束
    if ret_commit.returncode != 0:
        print("No changes detected; nothing to commit or push")
        print("==== Script finished ====")
        input("按回车退出...")
        raise SystemExit(0)

    # 4 git push
    print("\n[4/4] git push 推送至远程仓库")
    # ret_push = subprocess.run(["git", "push"])
    ret_push = subprocess.run(["git", "push", "-f"])

    if ret_push.returncode != 0:
        print("git push failed")
        input("按回车退出...")
        raise SystemExit(1)

    print("\nSync completed")
    print("==== Git sync finished ====")


if __name__ == "__main__":
    # 直接运行本文件测试用，示例前缀,
    git_auto_sync(commit_prefix="家脑_091006ok")
