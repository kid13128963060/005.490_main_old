import subprocess
from datetime import datetime

# ====================== 顶部配置区 ======================
# 仓库选择：1=005.490_main，2=005.490_main_old，3=两个仓库一起
select_mode = 3

repo_path_dict = {
    1: r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main",
    2: r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old",
}
commit_msg_template = "工脑新增一个脚本 {now_time}"
# ========================================================


def git_run(cmd_list, cwd_path):
    """执行git命令封装，cwd_path：git仓库路径"""
    proc = subprocess.run(cmd_list, cwd=cwd_path, capture_output=True, text=True, encoding="utf8")
    return proc


def sync_git_repo(repo_path):
    print(f"\n---------- 开始处理仓库：{repo_path} ----------")
    # git add .
    res_add = git_run(["git", "add", "."], repo_path)
    if res_add.returncode != 0:
        raise Exception(f"git add 失败：{res_add.stderr}")

    # 检查是否存在变更，git status --porcelain 有输出代表改动
    res_status = git_run(["git", "status", "--porcelain"], repo_path)
    if not res_status.stdout.strip():
        print("ℹ️ 没有检测到任何改动，无需提交推送")
        return

    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = commit_msg_template.format(now_time=now_time)

    res_commit = git_run(["git", "commit", "-m", commit_msg], repo_path)
    if res_commit.returncode != 0:
        raise Exception(f"commit失败：{res_commit.stderr}")

    # 推送：本地main → 远程main
    res_push = git_run(["git", "push", "origin", "main"], repo_path)
    if res_push.returncode != 0:
        raise Exception(f"push失败：{res_push.stderr}")
    print("✅ 推送成功！")


if __name__ == "__main__":
    run_list = []
    if select_mode == 1:
        run_list.append(repo_path_dict[1])
    elif select_mode == 2:
        run_list.append(repo_path_dict[2])
    elif select_mode == 3:
        run_list.append(repo_path_dict[1])
        run_list.append(repo_path_dict[2])
    else:
        print("❌ select_mode配置错误，请设置为 1 / 2 / 3")
        exit(1)

    for path in run_list:
        try:
            sync_git_repo(path)
        except Exception as e:
            print(f"❌ 当前仓库异常：{e}")
