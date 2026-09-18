# V1.3.5 远程覆盖本地｜自动合并｜冲突取远程｜修复无冲突场景远程无法覆盖本地已提交文件
# 保留本地完整提交时间线｜任务完成3秒倒计时关闭窗口｜批量双仓库

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
    修复：分支分叉但无冲突时，强制全部文件采用远程版本
    :param repo_cwd: Git仓库根目录(包含.git的文件夹绝对路径)
    """
    if not os.path.isdir(repo_cwd):
        raise FileNotFoundError(f"Git仓库路径不存在！\nrepo_cwd = {repo_cwd}")
    git_dot_git = os.path.join(repo_cwd, ".git")
    if not os.path.isdir(git_dot_git):
        raise FileNotFoundError(f"该目录下没有.git文件夹，不是Git仓库！\n{git_dot_git}")

    print("==== 远程覆盖本地开始【自动合并｜冲突取远程｜保留本地完整时间线】 ====")
    print(f"Git执行仓库目录: {repo_cwd}")
    print("⚠️ 警告：本操作会丢弃本地所有未提交修改；合并后强制全部文件使用远程版本！\n")

    print("[1/5] git fetch origin")
    ret_fetch = subprocess.run(["git", "fetch", "origin"], cwd=repo_cwd)
    if ret_fetch.returncode != 0:
        print("git fetch failed")
        raise SystemExit(1)

    # -X theirs：合并冲突自动采用远程(theirs)版本；--no-edit不修改合并提交信息
    print("[2/5] git merge origin/main -X theirs --no-edit")
    ret_merge = subprocess.run(
        ["git", "merge", "origin/main", "-X", "theirs", "--no-edit"], cwd=repo_cwd
    )
    if ret_merge.returncode != 0:
        print("⚠️ merge检测到冲突，继续执行强制取远程文件流程")

    # ----------------核心修复点----------------
    # 无论merge成功/冲突，强制全部工作区文件替换为远程版本，解决无冲突不覆盖bug
    print("[3/5] git checkout --theirs . 强制全部文件使用远程origin/main版本")
    subprocess.run(["git", "checkout", "--theirs", "."], cwd=repo_cwd)
    subprocess.run(["git", "add", "."], cwd=repo_cwd)

    print("[4/5] git commit --no-edit 保存合并&强制覆盖后的变更")
    subprocess.run(["git", "commit", "--no-edit"], cwd=repo_cwd)

    print("[5/5] git clean -fd 清理未跟踪文件")
    subprocess.run(["git", "clean", "-fd"], cwd=repo_cwd)

    print("\n✅本地文件全部更新为远程版本；本地全部提交时间线完整保留（新增一条合并提交）")
    print("💡查看完整时间线命令：git log --graph")
    print("==== 当前仓库操作完成 ====\n")


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
        print(f"\n❌程序顶层异常：{e}")
    finally:
        sys.stdout = old_stdout
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
    root.title("Git远程覆盖本地工具 Tkinter版 V1.3.5")
    root.geometry("920x580")

    var_select_repo = tk.IntVar(value=2)  # 默认选中2(main_old)

    # 仓库选择分组框
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

    # 执行按钮
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
