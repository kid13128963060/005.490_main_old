# V1.8.0 远程覆盖本地｜自动合并｜merge冲突取本地(-X ours)
# 保留本地时间线｜网络检测｜3秒倒计时，输入n回车取消关闭
# 批量双仓库｜任务锁防重复执行
import subprocess
import os
import tkinter as tk
from tkinter import scrolledtext
import threading
import socket

# --------------------------网络检测函数 socket原生--------------------------


def check_network(timeout=5):
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
    """print重定向写入日志框，**不再禁用控件**，保留用户输入权限"""

    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)

    def flush(self):
        pass


class GuiState:
    """全局状态：控制倒计时是否取消、任务是否正在运行"""

    def __init__(self):
        self.cancel_close = False
        self.task_running = False


def count_down_close(root, log_widget, state: GuiState):
    """3秒倒计时关闭，无弹窗；输入n回车取消关闭"""
    count = 3
    # 修复原模板bug：文案与实际倒计时统一为3秒
    log_widget.insert(tk.END, "\n====任务执行完毕====\n3秒后自动关闭窗口，在下方输入 n 按回车 保持窗口\n")
    log_widget.see(tk.END)

    def timer():
        nonlocal count
        if state.cancel_close:
            log_widget.insert(tk.END, ">>>收到指令 n，已取消自动关闭\n")
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


def on_log_enter(event, state: GuiState, log_widget):
    """回车事件：读取最后一行输入，检测是否为n"""
    if state.task_running:
        return
    last_line = log_widget.get("end-2l linestart", tk.END).strip().lower()
    if last_line == "n":
        state.cancel_close = True
        log_widget.delete("end-2l linestart", tk.END)


def git_remote_override_local(repo_cwd: str) -> None:
    """
    远程仓库变更合并到本地，冲突优先取本地版本(-X ours)，完整保留本地提交时间线
    :param repo_cwd: Git仓库根目录(包含.git的文件夹绝对路径)
    """
    if not os.path.isdir(repo_cwd):
        raise FileNotFoundError(f"Git仓库路径不存在！\nrepo_cwd = {repo_cwd}")
    git_dot_git = os.path.join(repo_cwd, ".git")
    if not os.path.isdir(git_dot_git):
        raise FileNotFoundError(f"该目录下没有.git文件夹，不是Git仓库！\n{git_dot_git}")

    print("==== 远程覆盖本地开始【自动合并｜冲突优先取本地｜保留本地时间线】 ====")
    print(f"Git执行仓库目录: {repo_cwd}")
    print("⚠️ 警告：建议先提交本地未提交修改\n")

    print("[1/3] git fetch origin")
    ret_fetch = subprocess.run(["git", "fetch", "origin"], cwd=repo_cwd)
    if ret_fetch.returncode != 0:
        print("git fetch failed")
        raise SystemExit(1)

    # 文档要求：merge策略冲突取本地 → 使用 -X ours
    print("[2/3] git merge origin/main -X ours --no-edit")
    ret_merge = subprocess.run(
        ["git", "merge", "origin/main", "-X", "ours", "--no-edit"], cwd=repo_cwd
    )
    if ret_merge.returncode != 0:
        print("⚠️ merge返回非0，尝试完成合并流程")

    print("[3/3] git clean -fd")
    subprocess.run(["git", "clean", "-fd"], cwd=repo_cwd)

    print("\n✅操作完成，本地全部提交时间线完整保留，冲突优先采用本地版本")
    print("==== 当前仓库操作完成 ====\n")


def run_override_task(log_widget, select_repo_value, root, state: GuiState):
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
        repo_list = []
        if select_repo_value == 1:
            repo_list = [REPO_1]
            print(f"✅ 选择仓库：005.490_main")
        elif select_repo_value == 2:
            repo_list = [REPO_2]
            print(f"✅ 选择仓库：005.490_main_old")
        elif select_repo_value == 3:
            repo_list = [REPO_1, REPO_2]
            print(f"✅ 选择：一次性处理全部两个仓库(005.490_main + 005.490_main_old)")
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
        root.after(0, lambda: count_down_close(root, log_widget, state))


def on_button_click(text_area, var_repo, root, state):
    """按钮点击回调，启动子线程"""
    if state.task_running:
        return
    selected = var_repo.get()
    t = threading.Thread(target=run_override_task,
                         args=(text_area, selected, root, state))
    t.daemon = True
    t.start()


def build_window():
    root = tk.Tk()
    root.title("Git远程覆盖本地工具 Tkinter版 V1.8.0")
    root.geometry("940x580")

    app_state = GuiState()
    var_select_repo = tk.IntVar(value=2)  # 默认选中2(main_old)

    frame_repo = tk.LabelFrame(
        root, text="选择Git目标仓库", font=("微软雅黑", 10))
    frame_repo.pack(padx=10, pady=6, fill=tk.X)

    tk.Radiobutton(frame_repo,
                   text="① 005.490_main仓库",
                   variable=var_select_repo,
                   value=1,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=12, pady=8)

    tk.Radiobutton(frame_repo,
                   text="② 005.490_main_old仓库",
                   variable=var_select_repo,
                   value=2,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=12, pady=8)

    tk.Radiobutton(frame_repo,
                   text="③ 一次性处理全部两个仓库",
                   variable=var_select_repo,
                   value=3,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=12, pady=8)

    btn_run = tk.Button(root, text="🔘执行远程仓库覆盖本地",
                        font=("微软雅黑", 11),
                        command=lambda: on_button_click(log_text, var_select_repo, root, app_state))
    btn_run.pack(pady=8)

    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)
    log_text.bind("<Return>", lambda e: on_log_enter(e, app_state, log_text))

    root.mainloop()


if __name__ == "__main__":
    build_window()

    # =========命令行脚本模式，取消注释即可直接运行不启动GUI=========
    # SELECT_REPO = 3
    # repo_list = []
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
