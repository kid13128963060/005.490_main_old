# V1.15.0 Git远程覆盖本地GUI工具｜merge冲突取远程｜无冲突也强制远程覆盖工作区文件｜保留本地时间线｜窗口5s自动执行｜执行完毕倒计时关闭｜Ctrl+C取消关闭｜批量双仓库｜任务锁防重复执行
# 变更记录：
# V1.9.0 修改merge策略 -X theirs，冲突优先采用远程版本；问题：仅冲突文件生效，无冲突文件不会被远程覆盖
# V1.10.0 修复：merge之后执行checkout origin/main -- . 强制全部工作区文件使用远程内容；完整保留本地commit提交时间线
# V1.15.0 ok 改良：窗口打开5秒自动执行任务；执行完毕保留倒计时关闭，控制台Ctrl+C可取消关闭；遵循docx全部约束
from Combination_Module.run_python_script import run_python_script, run_script_capture, run_script_get_stdout

import os
import signal
import socket
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext
from typing import List


# --------------------------网络检测函数 socket原生--------------------------
def check_network(timeout: int = 5) -> bool:
    """检测外网连通，True联网，False断网"""
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("223.5.5.5", 53))
        s.close()
        return True
    except Exception:
        return False


# --------------------------配置区--------------------------
REPO_1 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
REPO_2 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# -----------------------------------------------------------


class TextRedirector:
    """print重定向写入日志框，不再禁用控件，保留用户输入权限"""

    def __init__(self, widget: scrolledtext.ScrolledText) -> None:
        self.widget = widget

    def write(self, s: str) -> None:
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)

    def flush(self) -> None:
        pass


class GuiState:
    """全局状态：控制倒计时是否取消、任务是否正在运行、是否收到Ctrl+C信号"""

    def __init__(self) -> None:
        self.cancel_close: bool = False
        self.task_running: bool = False
        self.received_ctrl_c: bool = False


def sigint_handler(state: GuiState, root: tk.Tk) -> None:
    """捕获Ctrl+C(SIGINT)信号，标记取消倒计时关闭；Tkinter用after做线程安全UI调度"""
    state.received_ctrl_c = True
    state.cancel_close = True
    root.after(0, lambda: None)


def count_down_close(root: tk.Tk, log_widget: scrolledtext.ScrolledText, state: GuiState) -> None:
    """
    3秒倒计时关闭，无弹窗；控制台按下Ctrl+C可取消自动关闭；
    Tkinter after循环执行；收到Ctrl‑C标记则终止倒计时，保留窗口
    """
    count = 3
    log_widget.insert(
        tk.END,
        "\n====任务执行完毕====\n3秒后自动关闭窗口，控制台按下 Ctrl+C 可保持窗口\n",
    )
    log_widget.see(tk.END)

    def timer() -> None:
        nonlocal count
        if state.cancel_close:
            log_widget.insert(tk.END, ">>>收到 Ctrl+C，已取消自动关闭\n")
            log_widget.see(tk.END)
            return
        if count <= 0:
            root.destroy()
            return
        log_widget.insert(tk.END, f"倒计时 {count} s\n")
        log_widget.see(tk.END)
        count -= 1
        root.after(1000, timer)

    timer()


def git_remote_override_local(repo_cwd: str) -> None:
    """
    远程仓库变更合并到本地
    1. merge使用‑X theirs：发生冲突优先取远程版本
    2. checkout origin/main -- .：全部工作区文件强制使用远程内容，无冲突文件同样覆盖
    ✅完整保留本地所有commit提交时间线，不会删除本地提交
    :param repo_cwd: Git仓库根目录(包含.git的文件夹绝对路径)
    """
    if not os.path.isdir(repo_cwd):
        raise FileNotFoundError(f"Git仓库路径不存在！\nrepo_cwd = {repo_cwd}")
    git_dot_git = os.path.join(repo_cwd, ".git")
    if not os.path.isdir(git_dot_git):
        raise FileNotFoundError(f"该目录下没有.git文件夹，不是Git仓库！\n{git_dot_git}")

    print("==== 远程覆盖本地开始【自动合并｜冲突优先取远程｜全部工作区文件强制远程｜保留本地时间线】 ====")
    print(f"Git执行仓库目录: {repo_cwd}")
    print("⚠️ 警告：建议先提交本地未提交修改，未commit的工作区改动会被远程覆盖\n")

    print("[1/4] git fetch origin")
    ret_fetch = subprocess.run(["git", "fetch", "origin"], cwd=repo_cwd)
    if ret_fetch.returncode != 0:
        print("git fetch failed")
        raise SystemExit(1)

    # V1.9.0 merge策略冲突取远程 -X theirs
    print("[2/4] git merge origin/main -X theirs --no-edit")
    ret_merge = subprocess.run(["git", "merge", "origin/main", "-X", "theirs", "--no-edit"], cwd=repo_cwd)
    if ret_merge.returncode != 0:
        print("⚠️ merge返回非0，打印git status用于排查：")
        subprocess.run(["git", "status"], cwd=repo_cwd)

    # V1.10.0新增关键：强制工作区所有文件使用origin/main远程版本，不改动commit历史
    print("[3/4] git checkout origin/main -- . 强制工作区文件以远程为准")
    subprocess.run(["git", "checkout", "origin/main", "--", "."], cwd=repo_cwd)

    print("[4/4] git clean -fd 清除远程不存在的多余文件/文件夹")
    subprocess.run(["git", "clean", "-fd"], cwd=repo_cwd)

    print("\n✅操作完成，本地全部提交时间线完整保留，磁盘文件全部采用远程main版本")
    print("==== 当前仓库操作完成 ====\n")


def run_override_task(
    log_widget: scrolledtext.ScrolledText, select_repo_value: int, root: tk.Tk, state: GuiState
) -> None:
    """git业务逻辑，子线程运行"""
    import sys

    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    state.task_running = True
    try:
        print("🔍正在检测外网连通性...")
        if not check_network():
            print("❌外网断开，无法访问远程Git仓库，任务终止！")
            return
        print("✅网络正常\n")

        print("=====开始执行【远程覆盖本地】任务=====\n")
        repo_list: List[str] = []
        if select_repo_value == 1:
            repo_list = [REPO_1]
            print("✅ 选择仓库：005.490_main")
        elif select_repo_value == 2:
            repo_list = [REPO_2]
            print("✅ 选择仓库：005.490_main_old")
        elif select_repo_value == 3:
            repo_list = [REPO_1, REPO_2]
            print("✅ 选择：一次性处理全部两个仓库(005.490_main + 005.490_main_old)")
        else:
            raise ValueError("仅支持选项1、2、3")

        for idx, repo_path in enumerate(repo_list, 1):
            print(f"----------【第{idx}个仓库】{repo_path} ----------")
            try:
                git_remote_override_local(repo_cwd=repo_path)
            except Exception as e:
                print(f"❌ 当前仓库执行异常：{e}\n⚠️ 将继续处理下一个仓库\n")

        print("\n=====全部选定仓库处理流程结束=====")

    except Exception as e:
        print(f"\n程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        state.task_running = False
        state.cancel_close = False
        print("脚本执行完毕")
        root.after(0, lambda: count_down_close(root, log_widget, state))


def on_button_click(text_area: scrolledtext.ScrolledText, var_repo: tk.IntVar, root: tk.Tk, state: GuiState) -> None:
    """按钮点击回调，启动子线程；同时支持5秒窗口打开自动触发执行"""
    if state.task_running:
        return
    selected = var_repo.get()
    t = threading.Thread(target=run_override_task, args=(text_area, selected, root, state))
    t.daemon = True
    t.start()


def build_window() -> None:
    root = tk.Tk()
    root.title("Git远程覆盖本地工具 Tkinter版 V1.15.0")
    root.geometry("940x580")

    app_state = GuiState()
    # 注册SIGINT Ctrl+C信号处理器
    signal.signal(signal.SIGINT, lambda sig, frame: sigint_handler(app_state, root))

    var_select_repo = tk.IntVar(value=3)

    frame_repo = tk.LabelFrame(root, text="选择Git目标仓库", font=("微软雅黑", 10))
    frame_repo.pack(padx=10, pady=6, fill=tk.X)

    tk.Radiobutton(
        frame_repo,
        text="① 005.490_main仓库",
        variable=var_select_repo,
        value=1,
        font=("微软雅黑", 10),
    ).pack(side=tk.LEFT, padx=12, pady=8)

    tk.Radiobutton(
        frame_repo,
        text="② 005.490_main_old仓库",
        variable=var_select_repo,
        value=2,
        font=("微软雅黑", 10),
    ).pack(side=tk.LEFT, padx=12, pady=8)

    tk.Radiobutton(
        frame_repo,
        text="③ 一次性处理全部两个仓库",
        variable=var_select_repo,
        value=3,
        font=("微软雅黑", 10),
    ).pack(side=tk.LEFT, padx=12, pady=8)

    btn_run = tk.Button(
        root,
        text="🔘执行远程仓库覆盖本地",
        font=("微软雅黑", 11),
        command=lambda: on_button_click(log_text, var_select_repo, root, app_state),
    )
    btn_run.pack(pady=8)

    log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

    # 情况图1：窗口打开5秒自动执行任务，也支持手动按钮点击执行
    log_text.insert(tk.END, ">>>窗口已启动，将在5秒后自动开始执行任务，也可手动点击按钮立即执行\n")
    log_text.see(tk.END)
    root.after(5000, lambda: on_button_click(log_text, var_select_repo, root, app_state))

    root.mainloop()


if __name__ == "__main__":
    build_window()

    # =========命令行脚本模式，取消注释即可直接运行不启动GUI=========
    # SELECT_REPO = 3
    # repo_list: List[str] = []
    # if SELECT_REPO == 1:
    #     repo_list = [REPO_1]
    # elif SELECT_REPO == 2:
    #     repo_list = [REPO_2]
    # elif SELECT_REPO ==3:
    #     repo_list = [REPO_1,REPO_2]
    # else:
    #     raise ValueError("仅支持选项1、2、3")
    # for repo_path in repo_list:
    #     print(f"\n目标Git仓库路径：{repo_path}")
    #     git_remote_override_local(repo_cwd=repo_path)
    # print("脚本执行完毕")
