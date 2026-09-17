# V1.2.0 远程覆盖本地｜自动合并｜冲突取远程｜保留本地时间线｜任务完成3秒倒计时关闭窗口
import subprocess
import os
import tkinter as tk
from tkinter import scrolledtext
import threading

# --------------------------配置区【与git_gui模块完全保持一致】--------------------------
REPO_1 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main"
REPO_2 = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old"
# -----------------------------------------------------------------------------------


def countdown_close(log_widget, root, remain: int):
    """倒计时关闭窗口，**仅在tk主线程执行**"""
    if remain <= 0:
        root.destroy()
        return
    log_widget.configure(state="normal")
    log_widget.insert(tk.END, f"\n⏳ {remain}秒后自动关闭窗口...")
    log_widget.see(tk.END)
    log_widget.configure(state="disabled")
    root.after(1000, lambda: countdown_close(log_widget, root, remain - 1))


def git_remote_override_local(repo_cwd: str) -> None:
    """
    远程仓库覆盖本地：自动合并，冲突以远程版本为主，保留本地完整提交时间线
    :param repo_cwd: Git仓库根目录(包含.git的文件夹绝对路径)
    """
    if not os.path.isdir(repo_cwd):
        raise FileNotFoundError(f"Git仓库路径不存在！\nrepo_cwd = {repo_cwd}")
    git_dot_git = os.path.join(repo_cwd, ".git")
    if not os.path.isdir(git_dot_git):
        raise FileNotFoundError(f"该目录下没有.git文件夹，不是Git仓库！\n{git_dot_git}")

    print("==== 远程覆盖本地开始【自动合并｜冲突取远程｜保留本地时间线】 ====")
    print(f"Git执行仓库目录: {repo_cwd}")
    print("⚠️ 警告：本操作会丢弃本地所有未提交修改；合并冲突自动选用远程版本！\n")

    print("[1/3] git fetch origin")
    ret_fetch = subprocess.run(["git", "fetch", "origin"], cwd=repo_cwd)
    if ret_fetch.returncode != 0:
        print("git fetch failed")
        raise SystemExit(1)

    # -X theirs：合并冲突自动采用远程(theirs)版本；--no-edit不修改合并提交信息
    print("[2/3] git merge origin/main -X theirs --no-edit")
    ret_merge = subprocess.run(
        ["git", "merge", "origin/main", "-X", "theirs", "--no-edit"], cwd=repo_cwd
    )
    if ret_merge.returncode != 0:
        print("⚠️ merge返回非0，尝试完成合并流程")

    print("[3/3] git clean -fd")
    subprocess.run(["git", "clean", "-fd"], cwd=repo_cwd)

    print("\n✅本地文件已同步，本地全部提交时间线完整保留，冲突已自动选用远程版本")
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
    """子线程执行git任务，执行完毕后通过after调度主线程运行倒计时关闭"""
    import sys
    old_stdout = sys.stdout
    sys.stdout = TextRedirector(log_widget)
    try:
        print("=====开始执行【远程覆盖本地｜自动合并｜冲突取远程】任务=====\n")
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
        git_remote_override_local(repo_cwd=GIT_REPOSITORY)

    except Exception as e:
        print(f"\n❌程序异常：{e}")
    finally:
        sys.stdout = old_stdout
        # 【重点】子线程不能直接操作UI！用root.after把倒计时函数投递到主线程事件队列执行
        root.after(0, lambda: countdown_close(log_widget, root, remain=3))


def on_button_click(text_area, var_repo, root):
    """按钮点击回调，启动子线程执行任务，不阻塞UI；传入root窗口对象"""
    selected = var_repo.get()
    t = threading.Thread(target=run_override_task,
                         args=(text_area, selected, root))
    t.daemon = True
    t.start()


def build_window():
    root = tk.Tk()
    root.title("Git远程覆盖本地工具 Tkinter版 V1.2.0")
    root.geometry("780x560")

    var_select_repo = tk.IntVar(value=2)  # 默认选中2(main_old)

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

    # 执行按钮：把root实例传入回调函数
    btn_run = tk.Button(root, text="🔘执行远程仓库覆盖本地(自动合并，冲突取远程)",
                        font=("微软雅黑", 11),
                        command=lambda: on_button_click(log_text, var_select_repo, root))
    btn_run.pack(pady=8)

    # 滚动日志文本框
    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

    root.mainloop()


if __name__ == "__main__":
    # GUI图形界面模式（默认）
    build_window()

    # =========命令行脚本模式，取消注释即可直接运行不启动GUI=========
    # SELECT_REPO = 2
    # if SELECT_REPO == 1:
    #     GIT_REPOSITORY = REPO_1
    # elif SELECT_REPO == 2:
    #     GIT_REPOSITORY = REPO_2
    # else:
    #     raise ValueError("SELECT_REPO只能填写1或者2！1代表005.490_main，2代表005.490_main_old")
    # print(f"当前选择仓库编号 SELECT_REPO = {SELECT_REPO}")
    # print(f"目标Git仓库路径：{GIT_REPOSITORY}")
    # git_remote_override_local(repo_cwd=GIT_REPOSITORY)
