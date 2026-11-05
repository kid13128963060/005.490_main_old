import subprocess
from datetime import datetime

# 仓库绝对路径，根据实际环境修改
repo_path = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"


def git_run(cmd_list):
    """执行git命令封装"""
    proc = subprocess.run(cmd_list, cwd=repo_path, capture_output=True, text=True, encoding="utf‑8")
    return proc


try:
    # git add .
    res_add = git_run(["git", "add", "."])
    if res_add.returncode != 0:
        raise Exception(f"git add 失败：{res_add.stderr}")

    # 检查是否存在变更，git status --porcelain 有输出代表改动
    res_status = git_run(["git", "status", "--porcelain"])
    if not res_status.stdout.strip():
        print("ℹ️ 没有检测到任何改动，无需提交推送")
    else:
        commit_msg = f"自动同步 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        res_commit = git_run(["git", "commit", "-m", commit_msg])
        if res_commit.returncode != 0:
            raise Exception(f"commit失败：{res_commit.stderr}")

        # 推送：本地main → 远程005.490_main_old
        res_push = git_run(["git", "push", "origin", "main"])
        if res_push.returncode != 0:
            raise Exception(f"push失败：{res_push.stderr}")
        print("✅ 推送成功！")

except Exception as e:
    print(f"❌ 异常：{e}")
