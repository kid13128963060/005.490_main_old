import tkinter as tk
from tkinter import scrolledtext
import threading

from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync

# --------------------------配置区--------------------------
EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"
CommitPrefix = "old.一键保存关闭V1.0.03"

# 两个仓库路径
REPO_1 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
REPO_2 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# -----------------------------------------------------------


class TextRedirector:
    """把print打印重定向到tkinter文本框，控制台输出同步显示UI"""

    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")

    def flush(self):
        pass


def run_git_task(log_widget, select_repo_value):
    """
    实际执行git同步逻辑，运行在子线程
    :param log_widget:日志文本框
    :param select_repo_value:1=main仓库，2=main_old仓库
    """
    import sys
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    try:
        print("=====开始执行任务=====\n")
        CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
        print(f"读取到模拟器标识：{CELL_READ_CONST}")
        print(f"选定提交前缀：{CommitPrefix}")

        # 根据单选框的值选择仓库
        if select_repo_value == 1:
            GIT_REPOSITORY = REPO_1
            print("✅已选择仓库：005.490_main")
        elif select_repo_value == 2:
            GIT_REPOSITORY = REPO_2
            print("✅已选择仓库：005.490_main_old")
        else:
            raise ValueError("只能选择1或者2！")

        print(f"目标Git仓库路径：{GIT_REPOSITORY}")
        git_auto_sync(CommitPrefix, repo_cwd=GIT_REPOSITORY)

    except Exception as e:
        print(f"\n程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        print("\n====任务结束====\n")


def on_button_click(text_area, var_repo):
    """按钮点击回调，启动子线程执行git，不阻塞UI"""
    selected = var_repo.get()
    t = threading.Thread(target=run_git_task, args=(text_area, selected))
    t.daemon = True
    t.start()


def build_window():
    root = tk.Tk()
    root.title("Git一键同步工具 Tkinter版")
    root.geometry("780x540")

    # 绑定整型变量，用来接收单选框选择结果，默认选中2(main_old)
    var_select_repo = tk.IntVar(value=2)

    # 仓库选择区域（单选框）
    frame_repo = tk.LabelFrame(root, text="请选择Git目标仓库", font=("微软雅黑", 10))
    frame_repo.pack(padx=10, pady=6, fill=tk.X)

    tk.Radiobutton(frame_repo,
                   text="① 005.490_main 仓库",
                   variable=var_select_repo,
                   value=1,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=25, pady=8)

    tk.Radiobutton(frame_repo,
                   text="② 005.490_main_old 仓库",
                   variable=var_select_repo,
                   value=2,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=25, pady=8)

    # 执行按钮
    btn_run = tk.Button(root, text="🔘执行Git一键同步",
                        font=("微软雅黑", 11),
                        command=lambda: on_button_click(log_text, var_select_repo))
    btn_run.pack(pady=8)

    # 滚动日志文本框
    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

    root.mainloop()


if __name__ == "__main__":
    build_window()
