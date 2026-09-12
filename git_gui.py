import tkinter as tk
from tkinter import scrolledtext
import threading

from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync

# --------------------------配置区--------------------------
EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"
CommitPrefix = "old.测试GUI删多余文字"  # 提交前缀，方便在Git历史中区分

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
    """5秒倒计时关闭，无弹窗；输入n回车取消关闭"""
    count = 3
    log_widget.insert(tk.END, "\n====任务执行完毕====\n5秒后自动关闭窗口，在下方输入 n 按回车 保持窗口\n")
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
    # 任务未结束，忽略输入
    if state.task_running:
        return
    # 获取最后一行内容
    last_line = log_widget.get("end-2l linestart", tk.END).strip().lower()
    if last_line == "n":
        state.cancel_close = True
        # 清除输入的n，界面干净
        log_widget.delete("end-2l linestart", tk.END)


def run_git_task(log_widget, select_repo_value, root, state: GuiState):
    """git业务逻辑，子线程运行"""
    import sys
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    state.task_running = True
    try:
        print("=====开始执行任务=====\n")
        CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
        print(f"读取到模拟器标识：{CELL_READ_CONST}")
        print(f"选定提交前缀：{CommitPrefix}")

        if select_repo_value == 1:
            GIT_REPOSITORY = REPO_1
            print(f"✅ SELECT_REPO = {select_repo_value} 选择仓库：005.490_main")
        elif select_repo_value == 2:
            GIT_REPOSITORY = REPO_2
            print(f"✅ SELECT_REPO = {select_repo_value} 选择仓库：005.490_main_old")
        else:
            raise ValueError(
                "SELECT_REPO只能填写1或者2！1代表005.490_main，2代表005.490_main_old")

        print(f"目标Git仓库路径：{GIT_REPOSITORY}")
        git_auto_sync(CommitPrefix, repo_cwd=GIT_REPOSITORY)

    except Exception as e:
        print(f"\n程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        state.task_running = False
        state.cancel_close = False
        root.after(0, lambda: count_down_close(root, log_widget, state))


def on_button_click(text_area, var_repo, root, state):
    """按钮点击，启动子线程"""
    # 任务正在运行，禁止重复点击
    if state.task_running:
        return
    selected = var_repo.get()
    t = threading.Thread(target=run_git_task, args=(
        text_area, selected, root, state))
    t.daemon = True
    t.start()


def build_window():
    root = tk.Tk()
    root.title("Git一键同步工具 Tkinter版")
    root.geometry("780x560")

    app_state = GuiState()
    var_select_repo = tk.IntVar(value=2)  # 默认SELECT_REPO=2 main_old

    frame_repo = tk.LabelFrame(
        root, text="选择Git目标仓库（赋值SELECT_REPO）", font=("微软雅黑", 10))
    frame_repo.pack(padx=10, pady=6, fill=tk.X)

    tk.Radiobutton(frame_repo,
                   text="① SELECT_REPO=1 → 005.490_main仓库",
                   variable=var_select_repo,
                   value=1,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=20, pady=8)

    tk.Radiobutton(frame_repo,
                   text="② SELECT_REPO=2 → 005.490_main_old仓库",
                   variable=var_select_repo,
                   value=2,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=20, pady=8)

    btn_run = tk.Button(root, text="🔘执行Git一键同步",
                        font=("微软雅黑", 11),
                        command=lambda: on_button_click(log_text, var_select_repo, root, app_state))
    btn_run.pack(pady=8)

    # 重点：不再设置disabled，控件全程可编辑
    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)
    log_text.bind("<Return>", lambda e: on_log_enter(e, app_state, log_text))

    root.mainloop()


if __name__ == "__main__":
    build_window()
