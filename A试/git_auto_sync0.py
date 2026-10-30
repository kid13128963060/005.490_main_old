# V2.0.3 git自动同步模块；修复Windows下subprocess locale编码报错UnicodeEncodeError；
# 实现fetch、merge冲突取本地(-X ours)、提交；根据入参force_push判断是否使用--force强制推送，
# 接收GUI传入开关，异常向上抛出；二进制读取输出，errors=replace容错特殊字符
import os
import subprocess


def _run_git_cmd(cmd_list, cwd):
    """执行git命令，二进制读取stdout/stderr，手动解码容错，异常抛出；Windows静默不弹出黑窗口"""
    proc = subprocess.Popen(
        cmd_list,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW,  # 【新增】Windows静默，禁止弹出git黑窗口
    )
    out_bytes, err_bytes = proc.communicate()
    # 优先utf‑8解码，无法解析字符自动替换，防止UnicodeEncodeError崩溃
    out = out_bytes.decode("utf‑8", errors="replace")
    err = err_bytes.decode("utf‑8", errors="replace")
    print(out)
    if proc.returncode != 0:
        raise Exception(f"git命令失败：{' '.join(cmd_list)}\nstderr:{err}")  # noqa: TRY002
    return out


def git_auto_sync(commit_prefix: str, repo_cwd: str, force_push: bool = False):
    """
    git完整同步流程
    1.git fetch 拉取远端最新
    2.git merge origin/main -X ours 冲突优先保留本地代码
    3.git add全部变更
    4.git commit（有变更才提交）
    5.普通push / push --force 根据force_push参数决定
    """
    if not os.path.isdir(repo_cwd):
        raise FileNotFoundError(f"仓库路径不存在：{repo_cwd}")
    # 1 fetch 获取远端信息
    _run_git_cmd(["git", "fetch"], cwd=repo_cwd)
    # 合并远端，冲突取本地
    _run_git_cmd(["git", "merge", "origin/main", "-X", "ours"], cwd=repo_cwd)
    # add全部改动
    _run_git_cmd(["git", "add", "."], cwd=repo_cwd)
    # 检查是否有需要提交的变更
    status_out = _run_git_cmd(["git", "status", "--porcelain"], cwd=repo_cwd)
    if status_out.strip():
        commit_msg = f"{commit_prefix}"
        _run_git_cmd(["git", "commit", "-m", commit_msg], cwd=repo_cwd)
        # 根据参数选择是否强制推送
        if force_push:
            _run_git_cmd(["git", "push", "--force"], cwd=repo_cwd)
            print("✅ commit + 强制push执行完成")
        else:
            _run_git_cmd(["git", "push"], cwd=repo_cwd)
            print("✅ commit + 普通push执行完成")
    else:
        print("ℹ️ 没有本地变更，跳过commit、push")
