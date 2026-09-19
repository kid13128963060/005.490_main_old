# V1.0.4 Git回退指定commit并强制推送GUI工具｜单选框选仓库｜输入框填写commit哈希｜
# 日志重定向｜线程防卡死｜任务完成直接自动关闭窗口，移除3秒倒计时与n取消逻辑
# 变更记录：
# V1.0.1 增加仓库选择，支持外部目录运行测试（原始代码1）
# V1.0.2 新增Tkinter GUI界面；单选框控制SELECT_REPO；输入框控制TARGET_COMMIT_HASH；
#        print重定向日志；子线程防UI冻结；仓库/.git目录校验；异常捕获输出日志
# V1.0.3 移除3秒倒计时等待，任务执行完成直接自动关闭窗口，删除n取消关闭整套逻辑

import subprocess
import os
import tkinter as tk
from tkinter import scrolledtext
import threading


# ============仓库选择配置 1=main仓库，2=main_old仓库============
REPO_1 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
REPO_2 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# ==============================================================


class TextRedirector:
    """print重定向写入日志框，参考代码2实现"""
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)

    def flush(self):
        pass


class GuiState:
    """全局GUI状态：任务运行锁，防止重复点击执行"""
    def __init__(self):
        self.task_running = False


def run_git_command(cmd: list[str], cwd: str):
    """执行git命令，指定仓库工作目录，出错抛出异常，来自原始代码1"""
    print(f"执行命令: {' '.join(cmd)}")
    print(f"git执行工作目录(repo_cwd): {cwd}")
    # 前置路径校验
    if not os.path.isdir(cwd):
        raise FileNotFoundError(f"Git仓库路径不存在！cwd={cwd}")
    git_dotgit = os.path.join(cwd, ".git")
    if not os.path.isdir(git_dotgit):
        raise FileNotFoundError(f"目标目录不是git仓库，缺少.git文件夹 {git_dotgit}")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(
            f"命令失败:\nstdout:{result.stdout}\nstderr:{result.stderr}")
    print(result.stdout)


def git_reset_force_push(select_repo: int, target_commit_hash: str):
    """
    业务逻辑：git fetch -> reset --hard 指定commit -> push origin main --force
    :param select_repo: 1 主仓库 /2 old仓库
    :param target_commit_hash: 需要回退的commit哈希字符串
    """
    if select_repo == 1:
        GIT_REPOSITORY = REPO_1
    elif select_repo == 2:
        GIT_REPOSITORY = REPO_2
    else:
        raise ValueError("SELECT_REPO只能填写1或者2！1代表005.490_main，2代表005.490_main_old")

    if not target_commit_hash.strip():
        raise ValueError("TARGET_COMMIT_HASH提交哈希不能为空！请输入git commit完整哈希串")

    print(f"当前选择仓库编号 SELECT_REPO = {select_repo}")
    print(f"目标Git仓库路径：{GIT_REPOSITORY}")
    print(f"目标回退commit哈希：{target_commit_hash}")
    print("⚠️警告：将会清空本地未提交改动，强制覆盖远程main分支，仅单人仓库使用！\n")

    run_git_command(["git", "fetch", "origin"], cwd=GIT_REPOSITORY)
    run_git_command(["git", "reset", "--hard",
                     target_commit_hash], cwd=GIT_REPOSITORY)
    run_git_command(["git", "push", "origin", "main",
                     "--force"], cwd=GIT_REPOSITORY)

    print("✅ 已回退至 指定历史commit，并强制推送远程main")


def run_task_thread(log_widget, repo_radio_val, commit_hash_input, root, state: GuiState):
    """子线程运行git任务，避免UI阻塞；重定向print输出到日志控件"""
    import sys
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    state.task_running = True
    try:
        commit_hash = commit_hash_input.get().strip()
        print("=====开始执行【Git回退指定commit并强制推送】任务=====\n")
        git_reset_force_push(select_repo=repo_radio_val, target_commit_hash=commit_hash)
        print("\n====任务执行完毕，即将自动关闭窗口====\n")

    except Exception as e:
        print(f"\n❌ 回滚失败：{e}")
    finally:
        sys.stdout = old_stdout
        state.task_running = False
        # 直接关闭窗口，无倒计时，参考代码2 root.after调度UI操作
        root.after(0, lambda: root.destroy())


def on_execute_btn_click(text_area, var_repo, entry_hash, root, state):
    """执行按钮回调，启动后台线程"""
    if state.task_running:
        return
    sel_repo = var_repo.get()
    t = threading.Thread(target=run_task_thread,
                         args=(text_area, sel_repo, entry_hash, root, state))
    t.daemon = True
    t.start()


def build_gui_window():
    root = tk.Tk()
    root.title("Git回退指定Commit强制推送工具 V1.0.4")
    root.geometry("920x600")

    app_state = GuiState()
    var_select_repo = tk.IntVar(value=2)  # 默认选中2 main_old仓库

    # 单选框区域：控制变量1 SELECT_REPO
    frame_repo = tk.LabelFrame(root, text="选择Git目标仓库(控制变量SELECT_REPO)", font=("微软雅黑", 10))
    frame_repo.pack(padx=10, pady=6, fill=tk.X)

    tk.Radiobutton(frame_repo,
                   text="① 005.490_main仓库",
                   variable=var_select_repo,
                   value=1,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=15, pady=8)

    tk.Radiobutton(frame_repo,
                   text="② 005.490_main_old仓库",
                   variable=var_select_repo,
                   value=2,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=15, pady=8)

    # 输入框区域：控制变量2 TARGET_COMMIT_HASH
    frame_hash = tk.LabelFrame(root, text="目标Commit哈希(控制变量TARGET_COMMIT_HASH)", font=("微软雅黑", 10))
    frame_hash.pack(padx=10, pady=6, fill=tk.X)

    entry_commit_hash = tk.Entry(frame_hash, font=("Consolas",10))
    entry_commit_hash.pack(padx=10, pady=8, fill=tk.X)
    entry_commit_hash.insert(0, "2c6732b335ac46a24bc2b6af2e194b634ccea925")  # 默认原始hash值

    # 执行按钮
    btn_run = tk.Button(root, text="🔘执行回退并强制推送远程main",
                        font=("微软雅黑", 11),
                        fg="#bb2222",
                        command=lambda: on_execute_btn_click(log_text, var_select_repo, entry_commit_hash, root, app_state))
    btn_run.pack(pady=8)

    # 滚动日志输出框
    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

    root.mainloop()


if __name__ == "__main__":
    build_gui_window()

    # ============命令行模式(取消注释直接运行，不启动GUI界面)============
    # SELECT_REPO = 2
    # TARGET_COMMIT_HASH = "2c6732b335ac46a24bc2b6af2e194b634ccea925"
    # try:
    #     git_reset_force_push(SELECT_REPO, TARGET_COMMIT_HASH)
    # except Exception as e:
    #     print(f"❌ 回滚失败：{e}")
