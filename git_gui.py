import tkinter as tk
from tkinter import scrolledtext
import threading

from read_excel_const import read_simulator_cell
from git_auto_sync0 import git_auto_sync

# --------------------------配置区，和之前保持一致--------------------------
EXCEL_FILE = r"E:\自动同步_只增加\设备识别\设备识别.xls"
CommitPrefix = "old.一键保存关闭V1.0.03"
GIT_REPOSITORY = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# ---------------------------------------------------------------------------


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


def run_git_task(log_widget):
    """实际执行git同步逻辑，运行在子线程，防止窗口卡死"""
    import sys
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    try:
        print("=====开始执行任务=====\n")
        CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
        print(f"读取到模拟器标识：{CELL_READ_CONST}")
        print(f"选定提交前缀：{CommitPrefix}")
        git_auto_sync(CommitPrefix, repo_cwd=GIT_REPOSITORY)
    except Exception as e:
        print(f"\n程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        print("\n====任务结束====\n")


def on_button_click(text_area):
    """按钮点击回调，启动子线程执行git，不阻塞UI"""
    t = threading.Thread(target=run_git_task, args=(text_area,))
    t.daemon = True
    t.start()


def build_window():
    root = tk.Tk()
    root.title("Git一键同步工具 Tkinter版")
    root.geometry("750x500")  # 窗口大小宽×高

    # 1.按钮
    btn_run = tk.Button(root, text="🔘执行Git一键同步",
                        font=("微软雅黑", 11),
                        command=lambda: on_button_click(log_text))
    btn_run.pack(pady=8)

    # 2.滚动日志文本框（只读，展示print输出）
    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

    root.mainloop()


if __name__ == "__main__":
    build_window()
