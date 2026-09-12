import tkinter as tk
from tkinter import scrolledtext, simpledialog
import threading
import time

from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync

# --------------------------配置区--------------------------
EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"
CommitPrefix = "old.一键保存关闭V1.0.03"

REPO_1 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
REPO_2 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# -----------------------------------------------------------


class TextRedirector:
    """print重定向输出到UI日志框"""

    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")

    def flush(self):
        pass


def after_close_logic(root):
    """任务结束：弹出输入框，输入n则保留；否则5秒倒计时关闭窗口（运行在主线程）"""
    user_input = simpledialog.askstring("是否关闭窗口",
                                        "任务已完成！\n输入字母 n 回车 → 保持窗口不关闭\n直接点确定/取消 → 5秒后自动关闭")
    if user_input is not None and user_input.strip().lower() == "n":
        print("\n收到指令【n】，窗口保持打开，不自动关闭\n")
        return
    # 5秒倒计时关闭
    print("\n5秒后窗口将自动关闭...")
    count_down = 5

    def count():
        nonlocal count_down
        if count_down <= 0:
            root.destroy()
            return
        print(f"倒计时 {count_down} s")
        count_down -= 1
        root.after(1000, count)
    count()


def run_git_task(log_widget, select_repo_value, root):
    """git业务逻辑，子线程运行"""
    import sys
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    try:
        print("=====开始执行任务=====\n")
        CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
        print(f"读取到模拟器标识：{CELL_READ_CONST}")
        print(f"选定提交前缀：{CommitPrefix}")

        # 根据SELECT_REPO选择仓库
        if select_repo_value == 1:
            GIT_REPOSITORY = REPO_1
            print("✅已选择仓库：005.490_main 【SELECT_REPO=1】")
        elif select_repo_value == 2:
            GIT_REPOSITORY = REPO_2
            print("✅已选择仓库：005.490_main_old 【SELECT_REPO=2】")
        else:
            raise ValueError(
                "SELECT_REPO只能填写1或者2！1代表005.490_main，2代表005.490_main_old")

        print(f"目标Git仓库路径：{GIT_REPOSITORY}")
        git_auto_sync(CommitPrefix, repo_cwd=GIT_REPOSITORY)

    except Exception as e:
        print(f"\n程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        print("\n====任务结束====\n")
        # 把UI操作抛回主线程，子线程禁止直接操作tk控件
        root.after(0, lambda: after_close_logic(root))


def on_button_click(text_area, var_repo, root):
    """按钮点击回调，启动子线程"""
    selected = var_repo.get()
    t = threading.Thread(target=run_git_task, args=(text_area, selected, root))
    t.daemon = True
    t.start()


def build_window():
    root = tk.Tk()
    root.title("Git一键同步工具 Tkinter版")
    root.geometry("780x560")

    # SELECT_REPO 单选框变量，默认=2(main_old)
    var_select_repo = tk.IntVar(value=2)

    # 仓库选择分组框
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

    # 执行按钮
    btn_run = tk.Button(root, text="🔘执行Git一键同步",
                        font=("微软雅黑", 11),
                        command=lambda: on_button_click(log_text, var_select_repo, root))
    btn_run.pack(pady=8)

    # 日志滚动文本框
    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

    root.mainloop()


if __name__ == "__main__":
    build_window()
