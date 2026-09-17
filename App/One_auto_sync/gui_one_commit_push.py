# V1.0.0 本地推送远程｜提交注释输入框｜读取Excel模拟器标识
# 网络检测｜3秒倒计时，输入n回车取消关闭｜批量双仓库｜任务锁防重复执行
import tkinter as tk
from tkinter import scrolledtext
import threading
import socket

from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync

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
EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"
CommitPrefix = "old.测试中增加内置 socket 网络检测"  # 提交前缀，方便在Git历史中区分

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
    """3秒倒计时关闭，无弹窗；输入n回车取消关闭；修复模板文案bug统一为3秒"""
    count = 3
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


def run_git_task(log_widget, select_repo_value, commit_prefix_input, root, state: GuiState):
    """git业务逻辑，子线程运行，本地推送远程，支持批量仓库"""
    import sys
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    state.task_running = True
    # 使用界面输入；输入为空回退配置默认值
    use_prefix = commit_prefix_input.strip()
    if not use_prefix:
        use_prefix = CommitPrefix
    try:
        print("🔍正在检测外网连通性...")
        if not check_network():
            print("❌外网断开，无法访问远程Git仓库，任务终止！")
            return
        print("✅网络正常\n")

        print("=====开始执行【本地推送远程】任务=====\n")
        CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
        print(f"读取到模拟器标识：{CELL_READ_CONST}")
        print(f"选定提交前缀：{use_prefix}")

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
            print(f"\n----------【第{idx}个仓库】{repo_path} ----------")
            try:
                print(f"目标Git仓库路径：{repo_path}")
                # git_auto_sync内部：本地推送远程、merge冲突取本地版本(-X ours)
                git_auto_sync(use_prefix, repo_cwd=repo_path)
                print(f"==== 当前仓库操作完成 ====")
            except Exception as e:
                print(f"❌ 当前仓库执行异常：{e}\n⚠️ 将继续处理下一个仓库")

        print("\n=====全部选定仓库处理流程结束=====")

    except Exception as e:
        print(f"\n程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        state.task_running = False
        state.cancel_close = False
        root.after(0, lambda: count_down_close(root, log_widget, state))


def on_button_click(text_area, var_repo, entry_prefix, root, state):
    """按钮点击，接收输入框控件，启动子线程"""
    if state.task_running:
        return
    selected = var_repo.get()
    input_text = entry_prefix.get()
    t = threading.Thread(target=run_git_task, args=(
        text_area, selected, input_text, root, state))
    t.daemon = True
    t.start()


def build_window():
    root = tk.Tk()
    root.title("Git本地推送远程工具 Tkinter版 V1.0.0")
    root.geometry("960x640")

    app_state = GuiState()
    var_select_repo = tk.IntVar(value=2)  # 默认=2 main_old

    # =========新增CommitPrefix输入框UI=========
    frame_prefix = tk.LabelFrame(
        root, text="提交注释 CommitPrefix", font=("微软雅黑", 10))
    frame_prefix.pack(padx=10, pady=4, fill=tk.X)
    entry_commit = tk.Entry(frame_prefix, font=("Consolas", 10))
    entry_commit.pack(fill=tk.X, padx=8, pady=8)
    entry_commit.insert(0, CommitPrefix)

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

    btn_run = tk.Button(root, text="🔘执行Git本地推送远程",
                        font=("微软雅黑", 11),
                        command=lambda: on_button_click(log_text, var_select_repo, entry_commit, root, app_state))
    btn_run.pack(pady=8)

    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)
    log_text.bind("<Return>", lambda e: on_log_enter(e, app_state, log_text))

    root.mainloop()


if __name__ == "__main__":
    build_window()
