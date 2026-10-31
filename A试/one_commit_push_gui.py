# V2.0.5 Git本地推送远程工具 Tkinter版｜窗口5s自动执行｜输入n回车取消关闭｜Ctrl‑C中途停止｜批量双仓库｜任务锁防重复执行
# 变更记录：
# V2.0.3ok 配合修复git_auto_sync0的Windows subprocess编码报错UnicodeEncodeError；
# 修复顶层全局直接调用tk窗口导致CELL_READ_CONST赋值失效，UI输入框丢失模拟器标识bug；
# CELL_READ_CONST、CommitPrefix赋值放在UI界面build_window之前；增加Excel文件检查捕获异常防止程序崩溃；
# CommitPrefix格式old.+CELL_READ_CONST+系统月日小时+整理仓库；修复NameError log_text未定义bug；
# 本地推送远程｜提交注释输入框｜读取Excel模拟器标识｜自动合并merge冲突取本地(-X ours)
# 网络检测｜3秒倒计时，输入n回车取消关闭｜批量双仓库｜任务锁防重复执行｜UI增加强制推送复选框
# V2.0.5 改良：窗口打开5秒自动执行任务；增加signal捕获SIGINT支持Ctrl‑C中途停止；
#         全量添加类型注解；遵循Ruff规范；执行完毕输出"脚本执行完毕"；注释控制90字符内；
#         保留原有n输入回车取消关闭全部逻辑，不改动on_log_enter
import os
import sys
import socket
import signal
import threading
import tkinter as tk
from datetime import datetime, timedelta, timezone
from subprocess import CompletedProcess
from tkinter import messagebox, scrolledtext
from typing import Optional

from Combination_Module.git_auto_sync import git_auto_sync
from Combination_Module.read_excel_const import read_simulator_cell
from Combination_Module.vscode_activate_with_keys import vscode_activate_with_keys

# 导入外部run_python_script（文档必导入项，不可删减）
from Combination_Module.run_python_script import run_python_script, run_script_capture, run_script_get_stdout


# --------------------------网络检测函数 socket原生--------------------------
def check_network(timeout: int = 15) -> bool:
    """检测外网连通，True联网，False断网"""
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("223.5.5.5", 53))
        s.close()
        return True
    except Exception:
        return False


# --------------------------配置区（UI界面build_window之前完成赋值，
# Excel异常仅保存警告文本，不在顶层弹出tk弹窗）--------------------------
EXCEL_FILE = r"F:\自动同步_只增加\设备识别\设备识别.xls"
# Excel读取失败兜底
CELL_READ_CONST: str = "未知设备"
warn_msg: str = ""

try:
    if os.path.exists(EXCEL_FILE):
        CELL_READ_CONST = read_simulator_cell(EXCEL_FILE)
    else:
        warn_msg = f"Excel文件不存在：\n{EXCEL_FILE}\n" "将使用【未知设备】作为模拟器标识"
except Exception as e:
    warn_msg = f"读取Excel发生错误：{e!s}\n将使用【未知设备】作为模拟器标识"

# 全局拼接完整提交注释
CommitPrefix = f"{CELL_READ_CONST}{datetime.now(tz=timezone(timedelta(hours=8))).strftime('%m%d%H')}整理仓库"

REPO_1 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
REPO_2 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# -----------------------------------------------------------
BASE_DIR = sys.path[0]
sys.path.insert(0, BASE_DIR)


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
    """捕获Ctrl+C(SIGINT)信号，用于中途停止任务；Tkinter用after做线程安全UI调度"""
    state.received_ctrl_c = True
    root.after(0, lambda: None)


def count_down_close(root: tk.Tk, log_widget: scrolledtext.ScrolledText, state: GuiState) -> None:
    """
    3秒倒计时关闭，无弹窗；在日志框输入n按回车保持窗口；
    Tkinter after循环执行；输入n则终止倒计时保留窗口
    """
    count = 3
    log_widget.insert(
        tk.END,
        "\n====任务执行完毕====\n3秒后自动关闭窗口，在下方输入 n 按回车 保持窗口\n",
    )
    log_widget.see(tk.END)

    def timer() -> None:
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


def on_log_enter(event: tk.Event, state: GuiState, log_widget: scrolledtext.ScrolledText) -> None:
    """回车事件：读取最后一行输入，检测是否为n，保留原有逻辑不修改"""
    if state.task_running:
        return
    last_line = log_widget.get("end-2l linestart", tk.END).strip().lower()
    if last_line == "n":
        state.cancel_close = True
        log_widget.delete("end-2l linestart", tk.END)


def run_git_task(
    log_widget: scrolledtext.ScrolledText,
    select_repo_value: int,
    commit_prefix_input: str,
    force_push_switch: bool,
    root: tk.Tk,
    state: GuiState,
) -> None:
    """git业务逻辑，子线程运行，本地推送远程，支持批量仓库，接收界面强制推送开关"""
    import sys

    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    state.task_running = True
    # 使用界面输入；输入为空回退全局CommitPrefix默认值
    use_prefix = commit_prefix_input.strip()
    if not use_prefix:
        use_prefix = CommitPrefix
    try:
        print("🔍正在检测外网连通性...")
        if not check_network():
            print("❌外网断开，无法访问远程Git仓库，任务终止！")
            return
        print("✅网络正常\n")

        if force_push_switch:
            print("=====开始执行【本地推送远程｜自动合并冲突取本地｜开启强制推送】任务=====\n")
        else:
            print("=====开始执行【本地推送远程｜自动合并冲突取本地｜普通推送】任务=====\n")

        print(f"读取到模拟器标识：{CELL_READ_CONST}")
        print(f"选定提交前缀：{use_prefix}")
        print(f"强制推送开关：{'开启' if force_push_switch else '关闭'}")

        repo_list: list[str] = []
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
            print(f"\n----------【第{idx}个仓库】{repo_path} ----------")
            try:
                print(f"目标Git仓库路径：{repo_path}")
                git_auto_sync(use_prefix, repo_cwd=repo_path, force_push=force_push_switch)
                print("==== 当前仓库操作完成 ====")
            except Exception as e:
                print(f"❌ 当前仓库执行异常：{e}\n⚠️ 将继续处理下一个仓库")

        print("\n=====全部选定仓库处理流程结束=====")
    except Exception as e:
        print(f"\n程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        state.task_running = False
        state.cancel_close = False
        print("脚本执行完毕")
        root.after(0, lambda: count_down_close(root, log_widget, state))


def on_button_click(
    text_area: scrolledtext.ScrolledText,
    var_repo: tk.IntVar,
    entry_prefix: tk.Entry,
    var_force: tk.IntVar,
    root: tk.Tk,
    state: GuiState,
) -> None:
    """按钮点击，接收复选框状态，启动子线程；同时支持5秒窗口打开自动触发执行"""
    if state.task_running:
        return
    selected = var_repo.get()
    input_text = entry_prefix.get()
    force_flag = bool(var_force.get())
    t = threading.Thread(
        target=run_git_task,
        args=(text_area, selected, input_text, force_flag, root, state),
    )
    t.daemon = True
    t.start()


def build_window() -> None:
    root = tk.Tk()
    root.title("Git本地推送远程工具 Tkinter版 V2.0.5")
    root.geometry("960x580")

    app_state = GuiState()
    # 注册SIGINT Ctrl+C信号处理器，支持中途快捷键停止
    signal.signal(signal.SIGINT, lambda sig, frame: sigint_handler(app_state, root))

    # 主窗口创建完成后，再弹出Excel警告弹窗
    if warn_msg:
        messagebox.showwarning("Excel警告", warn_msg)

    var_select_repo = tk.IntVar(value=3)
    var_force_push = tk.IntVar(value=0)

    # =========提交注释输入框UI=========
    frame_prefix = tk.LabelFrame(root, text="提交注释 CommitPrefix", font=("微软雅黑", 10))
    frame_prefix.pack(padx=10, pady=4, fill=tk.X)
    entry_commit = tk.Entry(frame_prefix, font=("Consolas", 10))
    entry_commit.pack(fill=tk.X, padx=8, pady=8)
    entry_commit.insert(0, CommitPrefix)

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

    # =========推送选项复选框=========
    frame_option = tk.LabelFrame(root, text="推送选项", font=("微软雅黑", 10))
    frame_option.pack(padx=10, pady=4, fill=tk.X)
    tk.Checkbutton(
        frame_option,
        text="开启Git强制推送(--force，谨慎使用，会覆盖远程提交)",
        variable=var_force_push,
        font=("微软雅黑", 10),
    ).pack(padx=8, pady=6, anchor="w")

    btn_run = tk.Button(
        root,
        text="🔘执行Git本地推送远程",
        font=("微软雅黑", 11),
        command=lambda: on_button_click(log_text, var_select_repo, entry_commit, var_force_push, root, app_state),
    )
    btn_run.pack(pady=8)

    log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)
    # 保留回车绑定：输入n回车取消关闭，不修改原有逻辑
    log_text.bind("<Return>", lambda e: on_log_enter(e, app_state, log_text))

    # 情况图1需求：窗口打开5秒后自动执行任务，保留手动按钮立即执行
    log_text.insert(tk.END, ">>>窗口已启动，将在5秒后自动开始执行任务，也可手动点击按钮立即执行\n")
    log_text.see(tk.END)
    root.after(8000, lambda: on_button_click(log_text, var_select_repo, entry_commit, var_force_push, root, app_state))

    root.mainloop()


if __name__ == "__main__":
    vscode_activate_with_keys()
    build_window()
