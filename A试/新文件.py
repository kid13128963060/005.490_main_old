from datetime import datetime
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

try:
    # 使用绝对路径，防止相对路径定位错误，请确认路径和你电脑一致
    repo_path = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
    repo = Repo(repo_path)

    # ========== 等价 git add . （不使用 -A，不处理本地删除的文件） ==========
    repo.index.add(["."])
    # repo.index.remove([], working_tree=True)  # 禁用，不做git add -A行为
    # ======================================================================

    # 检查是否有改动，无改动就跳过commit、push，避免报错
    diff = repo.index.diff("HEAD")
    if not diff:
        print("ℹ️ 没有检测到任何改动，无需提交推送")
    else:
        # 本地提交
        commit_msg = f"自动同步 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        repo.index.commit(commit_msg)
        # 推送：本地main分支推送到远程 005.490_main_old
        origin = repo.remote("origin")
        push_result = origin.push("main:005.490_main_old")
        print("✅ 推送成功！结果：", push_result)

except InvalidGitRepositoryError:
    print("❌ 错误：指定目录不是合法Git仓库，请检查路径和里面的.git文件夹")
except GitCommandError as e:
    print("❌ Git执行失败：", e)
except Exception as e:
    print("❌ 其他异常：", e)
