# V1.0.1
import subprocess
import os
import tkinter as tk
from tkinter import scrolledtext
import threading

# --------------------------配置区【与git_gui模块完全保持一致】--------------------------
REPO_1 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
REPO_2 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# -----------------------------------------------------------------------------------


def git_remote_override_local(repo_cwd: str) -> None:
    """
    远程仓库强制覆盖本地文件
    :param repo_cwd: Git仓库根目录(包含.git的文件夹绝对路径)
    """
    # 前置校验，参考git_auto_sync0模块
    if not os.path.isdir(repo_cwd):
        raise FileNotFoundError(f"Git仓库路径不存在！\nrepo_cwd = {repo_cwd}")
    git_dot_git = os.path.join(repo_cwd, ".git")
    if not os.path.isdir(git_dot_git):
        raise FileNotFoundError(f"该目录下没有.git文件夹，不是Git仓库！\n{git_dot_git}")

    print("==== 远程覆盖本地开始 ====")
    print(f"Git执行仓库目录: {repo_cwd}")
    print("⚠️ 警告：本操作会丢弃本地所有未提交修改！\n")

    print("[1/3] git fetch origin")
    ret_fetch = subprocess.run(["git", "fetch", "origin"], cwd=repo_cwd)
    if ret_fetch.returncode != 0:
        print("git fetch failed")
        raise SystemExit(1)

    # 直接写 origin/main，不再依赖 origin/HEAD，规避指针损坏问题
    print("[2/3] git reset --hard origin/main")
    ret_reset = subprocess.run(
        ["git", "reset", "--hard", "origin/main"], cwd=repo_cwd)
    if ret_reset.returncode != 0:
        print("git reset failed")
        raise SystemExit(1)

    print("[3/3] git clean -fd")
    subprocess.run(["git", "clean", "-fd"], cwd=repo_cwd)

    print("\n✅本地文件已同步为远程最新版本")
    print("==== 操作完成 ====")


class TextRedirector:
    """把print打印重定向到tkinter文本框，控制台输出同步显示UI【复制自git_gui模块】"""

    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")

    def flush(self):
        pass


def run_override_task(log_widget, select_repo_value, root):
    """实际执行远程覆盖逻辑，运行在子线程，防止窗口卡死【仿照run_git_task】"""
    import sys
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    try:
        print("=====开始执行【远程覆盖本地】任务=====\n")

        # 条件判断选择仓库，和local_first_git_push.py逻辑保持一致
        if select_repo_value == 1:
            GIT_REPOSITORY = REPO_1
            print(f"✅ 选择仓库：005.490_main")
        elif select_repo_value == 2:
            GIT_REPOSITORY = REPO_2
            print(f"✅ 选择仓库：005.490_main_old")
        else:
            raise ValueError("只能选择1或者2！1代表005.490_main，2代表005.490_main_old")

        print(f"目标Git仓库路径：{GIT_REPOSITORY}")
        git_remote_override_local(repo_cwd=GIT_REPOSITORY)

    except Exception as e:
        print(f"\n程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        # 无论成功失败，主线程执行关闭窗口
        root.after(0, root.destroy)


def on_button_click(text_area, var_repo, root):
    """按钮点击回调，启动子线程执行任务，不阻塞UI【复制自git_gui】"""
    selected = var_repo.get()
    t = threading.Thread(target=run_override_task,
                         args=(text_area, selected, root))
    t.daemon = True
    t.start()


def build_window():
    root = tk.Tk()
    root.title("Git远程覆盖本地工具 Tkinter版")
    root.geometry("780x560")

    var_select_repo = tk.IntVar(value=2)  # 默认选中2(main_old)

    # 仓库选择分组框，UI移除SELECT_REPO文字
    frame_repo = tk.LabelFrame(
        root, text="选择Git目标仓库", font=("微软雅黑", 10))
    frame_repo.pack(padx=10, pady=6, fill=tk.X)

    tk.Radiobutton(frame_repo,
                   text="① 005.490_main仓库",
                   variable=var_select_repo,
                   value=1,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=20, pady=8)

    tk.Radiobutton(frame_repo,
                   text="② 005.490_main_old仓库",
                   variable=var_select_repo,
                   value=2,
                   font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=20, pady=8)

    # 执行按钮
    btn_run = tk.Button(root, text="🔘执行远程仓库覆盖本地",
                        font=("微软雅黑", 11),
                        command=lambda: on_button_click(log_text, var_select_repo, root))
    btn_run.pack(pady=8)

    # 滚动日志文本框，不绑定回车键
    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

    root.mainloop()


if __name__ == "__main__":
    # GUI图形界面模式（默认启动入口）
    build_window()

    # =========命令行脚本模式，取消注释即可直接运行不启动GUI=========
    # SELECT_REPO = 2
    # if SELECT_REPO == 1:
    #     GIT_REPOSITORY = REPO_1
    # elif SELECT_REPO == 2:
    #     GIT_REPOSITORY = REPO_2
    # else:
    #     raise ValueError("只能选择1或者2！1代表005.490_main，2代表005.490_main_old")
    # print(f"目标Git仓库路径：{GIT_REPOSITORY}")
    # git_remote_override_local(repo_cwd=GIT_REPOSITORY)
