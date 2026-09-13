import subprocess

# 定义目标提交哈希
TARGET_COMMIT_HASH = "71c8f40c52724b291e8b292b5288704ddafa151b"


def run_git_command(cmd: list[str]):
    """执行git命令，出错抛出异常"""
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"命令失败:\nstdout:{result.stdout}\nstderr:{result.stderr}")
    print(result.stdout)


if __name__ == "__main__":
    try:
        print("⚠️警告：将会清空本地未提交改动，强制覆盖远程main分支，仅单人仓库使用！")
        # git fetch origin
        run_git_command(["git", "fetch", "origin"])
        # git reset --hard 目标commit
        run_git_command(["git", "reset", "--hard", TARGET_COMMIT_HASH])
        # 强制推送到远程main
        run_git_command(["git", "push", "origin", "main", "--force"])
        print("✅ 已回退至 指定历史分支，并强制推送远程main")
    except Exception as e:
        print(f"❌ 回滚失败：{e}")
